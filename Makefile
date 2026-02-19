BIN_DIR    := $(HOME)/.local/bin
SKILLS_DIR := $(HOME)/.claude/skills
CREDS_DIR  := $(HOME)/.config/github-app

# Discover all skills under .claude/skills/
SKILLS := $(notdir $(wildcard .claude/skills/*))

.PHONY: install uninstall check help

help:
	@echo "Usage:"
	@echo "  make install    — install gh-token and link all Claude skills"
	@echo "  make uninstall  — remove installed files"
	@echo "  make check      — verify credentials and installation"

install: $(BIN_DIR)/gh-token $(addprefix $(SKILLS_DIR)/,$(SKILLS))
	@echo ""
	@echo "Done. Start Claude Code and use /github for authenticated GitHub ops."
	@if ! echo "$$PATH" | grep -q "$(BIN_DIR)"; then \
		echo ""; \
		echo "NOTE: $(BIN_DIR) is not in PATH. Add to your shell profile:"; \
		echo '  export PATH="$$HOME/.local/bin:$$PATH"'; \
	fi

$(BIN_DIR)/gh-token: scripts/gh-token.sh
	@mkdir -p $(BIN_DIR)
	cp $< $@
	chmod +x $@
	@echo "✓ $(BIN_DIR)/gh-token"

$(SKILLS_DIR)/%: .claude/skills/%
	@mkdir -p $(SKILLS_DIR)
	@rm -rf $(SKILLS_DIR)/$*
	ln -sf $(CURDIR)/.claude/skills/$* $(SKILLS_DIR)/$*
	@echo "✓ /$(notdir $*) skill → $(SKILLS_DIR)/$*"

uninstall:
	rm -f $(BIN_DIR)/gh-token
	$(foreach s,$(SKILLS),rm -rf $(SKILLS_DIR)/$(s);)
	@echo "✓ Uninstalled"

check:
	@echo "── gh-token ──────────────────────────────────"
	@test -x $(BIN_DIR)/gh-token \
		&& echo "✓ $(BIN_DIR)/gh-token installed" \
		|| echo "✗ not installed (run: make install)"
	@echo ""
	@echo "── GitHub App credentials ────────────────────"
	@test -f $(CREDS_DIR)/credentials \
		&& echo "✓ $(CREDS_DIR)/credentials" \
		|| echo "✗ missing $(CREDS_DIR)/credentials"
	@test -f $(CREDS_DIR)/private-key.pem \
		&& echo "✓ $(CREDS_DIR)/private-key.pem" \
		|| echo "✗ missing $(CREDS_DIR)/private-key.pem"
	@echo ""
	@echo "── Claude skills ─────────────────────────────"
	@$(foreach s,$(SKILLS), \
		test -e $(SKILLS_DIR)/$(s) \
			&& echo "✓ /$(s)" \
			|| echo "✗ /$(s) not linked"; \
	)
