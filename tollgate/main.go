package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"os/signal"

	"strings"
	"sync"
	"syscall"
	"time"
	"unsafe"

	"github.com/creack/pty"
	"github.com/fxamacker/cbor/v2"
	"github.com/gliderlabs/ssh"
	cryptossh "golang.org/x/crypto/ssh"
)

// --- Configuration ---

const (
	Port            = 22
	RateSecPerSat   = 60
	BaseDir         = "/opt/cashu-tollgate"
	WalletFile      = BaseDir + "/wallet.jsonl"
	TokensLogFile   = BaseDir + "/tokens.log"
	SpentHashesFile = BaseDir + "/spent.txt"
)

// --- Token Types ---

type TokenData struct {
	Mint   string     `json:"mint"`
	Unit   string     `json:"unit"`
	Memo   string     `json:"memo"`
	Amount int        `json:"amount"`
	Proofs []ProofEntry `json:"proofs"`
}

type ProofEntry struct {
	Amount int    `json:"amount"`
	ID     string `json:"id"`
	Secret string `json:"secret"`
	C      string `json:"C"`
}

// V4 CBOR types
type V4Token struct {
	Mint  string      `cbor:"m"`
	Unit  string      `cbor:"u"`
	Memo  string      `cbor:"d"`
	Token []V4Entry   `cbor:"t"`
}

type V4Entry struct {
	KeysetID []byte    `cbor:"i"`
	Proofs   []V4Proof `cbor:"p"`
}

type V4Proof struct {
	Amount int    `cbor:"a"`
	Secret string `cbor:"s"`
	C      []byte `cbor:"c"`
}

// V3 JSON types
type V3Token struct {
	Token []V3Mint `json:"token"`
	Unit  string   `json:"unit"`
	Memo  string   `json:"memo"`
}

type V3Mint struct {
	Mint   string    `json:"mint"`
	Proofs []V3Proof `json:"proofs"`
}

type V3Proof struct {
	Amount int    `json:"amount"`
	ID     string `json:"id"`
	Secret string `json:"secret"`
	C      string `json:"C"`
}

// Mint checkstate types
type CheckStateRequest struct {
	Proofs []struct {
		Secret string `json:"secret"`
	} `json:"proofs"`
}

type CheckStateResponse struct {
	States []struct {
		State string `json:"state"`
	} `json:"states"`
}

// --- Token Decoding ---

func b64urlDecode(s string) ([]byte, error) {
	// Add padding
	s = strings.ReplaceAll(s, "-", "+")
	s = strings.ReplaceAll(s, "_", "/")
	switch len(s) % 4 {
	case 2:
		s += "=="
	case 3:
		s += "="
	}
	return base64.StdEncoding.DecodeString(s)
}

func decodeCashuToken(tokenStr string) (*TokenData, error) {
	if strings.HasPrefix(tokenStr, "cashuB") {
		return decodeV4(tokenStr[6:])
	} else if strings.HasPrefix(tokenStr, "cashuA") {
		return decodeV3(tokenStr[6:])
	}
	return nil, fmt.Errorf("not a Cashu token (must start with cashuA or cashuB)")
}

func decodeV4(raw string) (*TokenData, error) {
	cborBytes, err := b64urlDecode(raw)
	if err != nil {
		return nil, fmt.Errorf("V4 base64 decode error: %w", err)
	}

	var v4 V4Token
	if err := cbor.Unmarshal(cborBytes, &v4); err != nil {
		return nil, fmt.Errorf("V4 CBOR decode error: %w", err)
	}

	if v4.Mint == "" {
		return nil, fmt.Errorf("token has no mint URL")
	}

	var proofs []ProofEntry
	amount := 0
	for _, entry := range v4.Token {
		for _, p := range entry.Proofs {
			amount += p.Amount
			proofs = append(proofs, ProofEntry{
				Amount: p.Amount,
				ID:     fmt.Sprintf("%x", entry.KeysetID),
				Secret: p.Secret,
				C:      fmt.Sprintf("%x", p.C),
			})
		}
	}

	if amount == 0 {
		return nil, fmt.Errorf("token has zero value")
	}

	return &TokenData{
		Mint:   v4.Mint,
		Unit:   v4.Unit,
		Memo:   v4.Memo,
		Amount: amount,
		Proofs: proofs,
	}, nil
}

func decodeV3(raw string) (*TokenData, error) {
	jsonBytes, err := b64urlDecode(raw)
	if err != nil {
		return nil, fmt.Errorf("V3 base64 decode error: %w", err)
	}

	var v3 V3Token
	if err := json.Unmarshal(jsonBytes, &v3); err != nil {
		return nil, fmt.Errorf("V3 JSON decode error: %w", err)
	}

	var proofs []ProofEntry
	amount := 0
	mint := ""
	for _, t := range v3.Token {
		if t.Mint != "" {
			mint = t.Mint
		}
		for _, p := range t.Proofs {
			amount += p.Amount
			proofs = append(proofs, ProofEntry{
				Amount: p.Amount,
				ID:     p.ID,
				Secret: p.Secret,
				C:      p.C,
			})
		}
	}

	if amount == 0 {
		return nil, fmt.Errorf("token has zero value")
	}
	if mint == "" {
		return nil, fmt.Errorf("token has no mint URL")
	}

	return &TokenData{
		Mint:   mint,
		Unit:   v3.Unit,
		Memo:   v3.Memo,
		Amount: amount,
		Proofs: proofs,
	}, nil
}

// --- Mint Verification ---

func verifyWithMint(tokenData *TokenData) (bool, string) {
	mintURL := strings.TrimRight(tokenData.Mint, "/")
	isTest := strings.Contains(strings.ToLower(mintURL), "test")

	if !strings.HasPrefix(mintURL, "http") {
		return false, "Invalid mint URL"
	}

	if !isTest {
		log.Printf("Real-mint token (no enforcement): %s", mintURL)
		return true, "OK"
	}

	// Test mint: verify unspent
	reqBody := CheckStateRequest{}
	for _, p := range tokenData.Proofs {
		reqBody.Proofs = append(reqBody.Proofs, struct {
			Secret string `json:"secret"`
		}{Secret: p.Secret})
	}

	bodyBytes, err := json.Marshal(reqBody)
	if err != nil {
		return false, fmt.Sprintf("JSON error: %v", err)
	}

	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Post(mintURL+"/v1/checkstate", "application/json", bytes.NewReader(bodyBytes))
	if err != nil {
		return false, fmt.Sprintf("Mint unreachable: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return false, fmt.Sprintf("Mint error: HTTP %d", resp.StatusCode)
	}

	var result CheckStateResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return false, fmt.Sprintf("Mint response parse error: %v", err)
	}

	for _, s := range result.States {
		if s.State != "UNSPENT" {
			return false, "Token already spent"
		}
	}

	return true, "OK"
}

// --- Wallet & Logging ---

func tokenHash(tokenStr string) string {
	h := sha256.Sum256([]byte(tokenStr))
	return fmt.Sprintf("%x", h)
}

func isTokenSpent(thash string) bool {
	data, err := os.ReadFile(SpentHashesFile)
	if err != nil {
		return false
	}
	return strings.Contains(string(data), thash)
}

func markSpent(thash string) {
	f, err := os.OpenFile(SpentHashesFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return
	}
	defer f.Close()
	f.WriteString(thash + "\n")
}

func logToken(tokenStr string, tokenData *TokenData, guest string, accepted bool) {
	entry := map[string]interface{}{
		"ts":       time.Now().UTC().Format(time.RFC3339),
		"guest":    guest,
		"accepted": accepted,
		"mint":     tokenData.Mint,
		"amount":   tokenData.Amount,
		"unit":     tokenData.Unit,
		"hash":     tokenHash(tokenStr),
	}
	f, err := os.OpenFile(TokensLogFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return
	}
	defer f.Close()
	line, _ := json.Marshal(entry)
	f.WriteString(string(line) + "\n")
}

func storeInWallet(tokenStr string, tokenData *TokenData) {
	entry := map[string]interface{}{
		"ts":     time.Now().UTC().Format(time.RFC3339),
		"mint":   tokenData.Mint,
		"amount": tokenData.Amount,
		"unit":   tokenData.Unit,
		"token":  tokenStr,
	}
	f, err := os.OpenFile(WalletFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return
	}
	defer f.Close()
	line, _ := json.Marshal(entry)
	f.WriteString(string(line) + "\n")
	log.Printf("Wallet +%d %s from %s", tokenData.Amount, tokenData.Unit, tokenData.Mint)
}

// --- Guest User Management ---

func guestUsername(tokenStr string) string {
	return "g-" + tokenHash(tokenStr)[:8]
}

func createGuestUser(name string) error {
	cmd := exec.Command("useradd", "-m", "-d", "/home/"+name, "-s", "/bin/bash", name)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("useradd failed: %s: %w", strings.TrimSpace(string(out)), err)
	}

	home := "/home/" + name
	exec.Command("chmod", "700", home).Run()

	bashrc := "export PS1=\"\\u@tollgate:\\w\\$ \"\nexport PATH=\"/usr/local/bin:/usr/bin:/bin:/usr/games\"\n"
	rcPath := home + "/.bashrc"
	os.WriteFile(rcPath, []byte(bashrc), 0644)
	exec.Command("chown", name+":"+name, rcPath).Run()

	return nil
}

func cleanupGuest(name string) {
	log.Printf("Cleaning up guest: %s", name)
	exec.Command("pkill", "-u", name).Run()
	exec.Command("userdel", "-r", "-f", name).Run()
}

func redeemToken(tokenStr string) (int, error) {
	cmd := exec.Command(
		"sudo", "-u", "cashu-wallet",
		"cdk-cli",
		"--work-dir", "/var/lib/cashu-wallet",
		"receive",
		"--allow-untrusted",
		tokenStr,
	)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return 0, fmt.Errorf("cdk-cli receive failed: %s: %w", strings.TrimSpace(string(out)), err)
	}
	result := strings.TrimSpace(string(out))
	log.Printf("cdk-cli receive: %s", result)
	return 0, nil
}

// --- PTY Window Resize ---

func setWinsize(f *os.File, w, h int) {
	syscall.Syscall(
		syscall.SYS_IOCTL,
		f.Fd(),
		uintptr(syscall.TIOCSWINSZ),
		uintptr(unsafe.Pointer(&struct{ h, w, x, y uint16 }{
			uint16(h), uint16(w), 0, 0,
		})),
	)
}

// --- Session Metadata ---

type SessionMeta struct {
	Started  float64 `json:"started"`
	Duration int     `json:"duration"`
	Guest    string  `json:"guest"`
	Mint     string  `json:"mint"`
	Amount   int     `json:"amount"`
}

func writeSessionMeta(guest string, tokenData *TokenData, seconds int) {
	meta := SessionMeta{
		Started:  float64(time.Now().UnixMilli()) / 1000.0,
		Duration: seconds,
		Guest:    guest,
		Mint:     tokenData.Mint,
		Amount:   tokenData.Amount,
	}
	data, _ := json.Marshal(meta)
	path := "/home/" + guest + "/.tollgate"
	os.WriteFile(path, data, 0600)
	exec.Command("chown", guest+":"+guest, path).Run()
}

// --- MOTD ---

func renderMOTD(tokenData *TokenData, guest string, seconds int) string {
	minutes := tokenData.Amount
	isTest := strings.Contains(strings.ToLower(tokenData.Mint), "test")
	mintDisplay := tokenData.Mint
	if len(mintDisplay) > 36 {
		mintDisplay = mintDisplay[:33] + "..."
	}
	testStr := "NO"
	if isTest {
		testStr = "YES"
	}

	return fmt.Sprintf(
		"\r\n"+
			"  +======================================+\r\n"+
			"  |        CASHU TOLLGATE                |\r\n"+
			"  +======================================+\r\n"+
			"  |  Mint:   %-28s |\r\n"+
			"  |  Amount: %4d %-23s |\r\n"+
			"  |  Time:   %4d min (%5d sec)       |\r\n"+
			"  |  User:   %-28s |\r\n"+
			"  |  Test:   %-28s |\r\n"+
			"  +======================================+\r\n"+
			"  |  Run 'timeleft' to see remaining time|\r\n"+
			"  |  Session self-destructs on timeout.  |\r\n"+
			"  +======================================+\r\n"+
			"\r\n",
		mintDisplay, minutes, tokenData.Unit, minutes, seconds, guest, testStr,
	)
}

// --- Spent hash file lock ---

var spentMu sync.Mutex

func isTokenSpentSafe(thash string) bool {
	spentMu.Lock()
	defer spentMu.Unlock()
	return isTokenSpent(thash)
}

func markSpentSafe(thash string) {
	spentMu.Lock()
	defer spentMu.Unlock()
	markSpent(thash)
}

// --- Main ---

func main() {
	os.MkdirAll(BaseDir, 0755)

	ssh.Handle(func(s ssh.Session) {
		username := s.User()
		log.Printf("Session request from %s, user=%d chars", s.RemoteAddr(), len(username))

		// 1. Decode token
		tokenData, err := decodeCashuToken(username)
		if err != nil {
			io.WriteString(s, fmt.Sprintf("\r\nError: %s\r\n\r\n", err))
			s.Exit(1)
			return
		}

		thash := tokenHash(username)
		guest := guestUsername(username)
		seconds := tokenData.Amount * RateSecPerSat

		// 2. Check replay
		if isTokenSpentSafe(thash) {
			io.WriteString(s, "\r\nError: token already used\r\n\r\n")
			s.Exit(1)
			return
		}

		// 3. Verify with mint
		ok, msg := verifyWithMint(tokenData)
		if !ok {
			logToken(username, tokenData, guest, false)
			io.WriteString(s, fmt.Sprintf("\r\nError: %s\r\n\r\n", msg))
			s.Exit(1)
			return
		}

		// 4. Redeem token to wallet
		io.WriteString(s, "  Redeeming token...\r\n")
		if _, err := redeemToken(username); err != nil {
			log.Printf("Token redemption failed: %v", err)
			logToken(username, tokenData, guest, false)
			io.WriteString(s, fmt.Sprintf("\r\nError: token redemption failed\r\n\r\n"))
			s.Exit(1)
			return
		}
		log.Printf("Token redeemed to wallet: %d sat from %s", tokenData.Amount, tokenData.Mint)

		// 5. Mark spent & log
		markSpentSafe(thash)
		logToken(username, tokenData, guest, true)

		// 6. Create guest user
		if err := createGuestUser(guest); err != nil {
			log.Printf("Failed to create guest: %v", err)
			io.WriteString(s, "\r\nError: could not create guest account\r\n\r\n")
			s.Exit(1)
			return
		}

		// 7. Write session metadata
		writeSessionMeta(guest, tokenData, seconds)

		// 8. MOTD
		io.WriteString(s, renderMOTD(tokenData, guest, seconds))

		// 9. Spawn bash as guest inside a PTY
		ptyReq, winCh, isPty := s.Pty()
		cmd := exec.Command("sudo", "-u", guest, "-H", "bash", "-i")
		if isPty {
			cmd.Env = append(cmd.Env, fmt.Sprintf("TERM=%s", ptyReq.Term))
		}

		ptmx, err := pty.Start(cmd)
		if err != nil {
			log.Printf("PTY start failed: %v", err)
			cleanupGuest(guest)
			io.WriteString(s, "\r\nError: could not start shell\r\n\r\n")
			s.Exit(1)
			return
		}

		log.Printf("Bash PID=%d started for %s", cmd.Process.Pid, guest)

		done := make(chan struct{})
		cleanupOnce := sync.Once{}
		cleanup := func() {
			cleanupOnce.Do(func() {
				ptmx.Close()
				cmd.Process.Kill()
				cmd.Wait()
				s.Close()
				cleanupGuest(guest)
				log.Printf("Session ended: %s", guest)
			})
		}
		defer cleanup()

		go func() {
			for win := range winCh {
				setWinsize(ptmx, win.Width, win.Height)
			}
		}()

		go func() {
			select {
			case <-time.After(time.Duration(seconds) * time.Second):
				log.Printf("Time's up: %s", guest)
				io.WriteString(s, "\r\n=== Time's up! Session ending. ===\r\n")
				cmd.Process.Signal(syscall.SIGTERM)
				time.Sleep(500 * time.Millisecond)
				cleanup()
			case <-done:
			}
		}()

		go func() {
			io.Copy(ptmx, s)
			close(done)
		}()

		io.Copy(s, ptmx)
		close(done)
	})

	// Load host keys
	hostKeys := []string{
		"/etc/ssh/ssh_host_ed25519_key",
		"/etc/ssh/ssh_host_rsa_key",
	}
	var signers []ssh.Signer
	for _, keyPath := range hostKeys {
		keyBytes, err := os.ReadFile(keyPath)
		if err != nil {
			log.Printf("Warning: could not read host key %s: %v", keyPath, err)
			continue
		}
		signer, err := cryptossh.ParsePrivateKey(keyBytes)
		if err != nil {
			log.Printf("Warning: could not parse host key %s: %v", keyPath, err)
			continue
		}
		signers = append(signers, signer)
	}
	if len(signers) == 0 {
		log.Fatal("No SSH host keys found!")
	}

	server := &ssh.Server{
		Addr:    fmt.Sprintf(":%d", Port),
		Handler: ssh.DefaultHandler,
	}
	for _, s := range signers {
		server.AddHostKey(s)
	}

	// No auth - accept any username (the token IS the auth)

	log.Printf("Cashu Tollgate listening on port %d", Port)
	log.Printf("Wallet: %s", WalletFile)
	log.Printf("Token log: %s", TokensLogFile)

	// Graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigChan
		log.Println("Shutting down...")
		server.Close()
	}()

	if err := server.ListenAndServe(); err != nil && err != ssh.ErrServerClosed {
		log.Fatalf("Server error: %v", err)
	}
}
