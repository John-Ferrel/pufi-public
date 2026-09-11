#!/usr/bin/env bash
# ============================================================================
# Pufi install script — private or public edition (auto-detected).
#
# Installs the Pufi persona + skills into an OpenCode config directory:
#   global  → ~/.config/opencode/            (all projects)
#   project → <repo>/.opencode/              (this repo only)
#   custom  → any directory, e.g. <ws>/.opencode via --opencode-dir
#
# Edition is detected from the tree: a clone containing pufi-nsfw/ is the
# private edition (full persona); the built public tree is light-only.
# For project/custom targets the workspace opencode.json is auto-merged with
# default_agent + external_directory permissions (see action_config).
#
# Usage:
#   ./install.sh                          # fully interactive
#   ./install.sh --target global --persona full --skill all --yes
#   ./install.sh --target custom --opencode-dir /path/to/ws/.opencode --yes
#   ./install.sh --setup-env              # (re)configure API env files
#   ./install.sh --smoke                  # dry-run smoke test of installed skills
#   ./install.sh doctor                   # inspect what is (not) installed
#   ./install.sh uninstall                # remove what this script installed
#   ./install.sh --help
# ============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIG_BASE="${XDG_CONFIG_HOME:-$HOME/.config}"
OPENCODE_DIR="$CONFIG_BASE/opencode"
GLOBAL_AGENT_DIR="$OPENCODE_DIR/agents"
GLOBAL_SKILL_DIR="$OPENCODE_DIR/skills"
PROJECT_AGENT_DIR="$REPO_DIR/.opencode/agents"
PROJECT_SKILL_DIR="$REPO_DIR/.opencode/skills"
PUFI_CONFIG_DIR="$CONFIG_BASE/pufi"

# ---- edition ---------------------------------------------------------------

if [[ -f "$REPO_DIR/pufi-nsfw/pufi.md" ]]; then
  EDITION="private"
else
  EDITION="public"
fi

# ---- defaults / flags ------------------------------------------------------

TARGET=""            # global | project | custom ("" = ask)
SKILLS=""            # all | pufi-image | pufi-anime ("" = ask)
PERSONA=""           # full | light ("" = ask; private defaults full, public light)
CUSTOM_DIR=""        # --opencode-dir target for custom installs
ASSUME_YES=0
DRY_RUN=0
ACTION="install"     # install | setup_env | smoke | doctor | uninstall

usage() {
  echo "Pufi install script — private or public edition (auto-detected)"
  echo
  echo "Installs the Pufi persona + skills into an OpenCode config directory:"
  echo "  global  → ~/.config/opencode/"
  echo "  project → <repo>/.opencode/"
  echo "  custom  → any directory via --opencode-dir"
  echo
  echo "Usage:"
  echo "  ./install.sh                          # fully interactive"
  echo "  ./install.sh --target global --persona full --skill all --yes"
  echo "  ./install.sh --target custom --opencode-dir /path/to/ws/.opencode --yes"
  echo "  ./install.sh --setup-env              # (re)configure API env files"
  echo "  ./install.sh --smoke                  # dry-run smoke test of installed skills"
  echo "  ./install.sh doctor                   # inspect what is (not) installed"
  echo "  ./install.sh uninstall                # remove what this script installed"
  echo
  echo "Options:"
  echo "  --target <global|project|custom>   install location (default: ask)"
  echo "  --opencode-dir <path>              custom opencode config dir (implies --target custom)"
  echo "  --persona <full|light>             full = complete persona (private only)"
  echo "  --skill <all|pufi-image|pufi-anime>  which skills to deploy (default: ask)"
  echo "  --setup-env                        (re)configure ~/.config/pufi/*.env interactively"
  echo "  --smoke                            dry-run smoke test of deployed skills"
  echo "  --yes                              skip confirmation prompts"
  echo "  --dry-run                          print the plan without writing anything"
  echo "  doctor                             inspect deployment state"
  echo "  uninstall                          remove what this script installed"
  echo "  --help                             show this help"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)   TARGET="$2"; shift 2 ;;
    --opencode-dir) CUSTOM_DIR="$2"; shift 2 ;;
    --persona)  PERSONA="$2"; shift 2 ;;
    --skill)    SKILLS="$2"; shift 2 ;;
    --setup-env) ACTION="setup_env"; shift ;;
    --smoke)     ACTION="smoke"; shift ;;
    --yes)       ASSUME_YES=1; shift ;;
    --dry-run)   DRY_RUN=1; shift ;;
    doctor)      ACTION="doctor"; shift ;;
    uninstall)   ACTION="uninstall"; shift ;;
    --help|-h)   usage; exit 0 ;;
    *) echo "[!] unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

# ---- helpers ---------------------------------------------------------------

log()  { printf '\033[1;34m[Pufi]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[!]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[!] %s\033[0m\n' "$*" >&2; exit 1; }

ask() { # ask <prompt> <default>
  local prompt="$1" def="${2:-}"
  if [[ -n "$def" ]]; then
    read -r -p "$prompt [$def]: " ans
    printf '%s\n' "${ans:-$def}"
  else
    read -r -p "$prompt: " ans
    printf '%s\n' "$ans"
  fi
}

confirm() { # confirm <description>
  [[ $ASSUME_YES -eq 1 ]] && return 0
  local desc="$1"
  read -r -p "  Apply: $desc ? [y/N] " ans
  [[ "${ans,,}" == "y" || "${ans,,}" == "yes" ]]
}

# ---- resolution ------------------------------------------------------------

resolve_target() {
  if [[ -z "$TARGET" && $ASSUME_YES -eq 1 ]]; then
    TARGET="global"
  fi
  if [[ -n "$TARGET" ]]; then
    case "$TARGET" in
      global|project) return ;;
      custom)
        if [[ -z "$CUSTOM_DIR" ]]; then
          if [[ $ASSUME_YES -eq 1 ]]; then
            die "--target custom requires --opencode-dir <path> when using --yes"
          fi
          OPENCODE_DIR="$(ask "Custom opencode config dir (agents/skills live under it)" "$OPENCODE_DIR")"
          GLOBAL_AGENT_DIR="$OPENCODE_DIR/agents"
          GLOBAL_SKILL_DIR="$OPENCODE_DIR/skills"
        fi
        return
        ;;
      *) die "bad --target: $TARGET (global|project|custom)" ;;
    esac
  fi
  echo "Where should Pufi be installed?"
  echo "  1) global   → $GLOBAL_AGENT_DIR + $GLOBAL_SKILL_DIR (all projects)"
  echo "  2) project  → $PROJECT_AGENT_DIR + $PROJECT_SKILL_DIR (this repo only)"
  echo "  3) custom   → enter your own opencode config dir (e.g. <workspace>/.opencode)"
  local c; c="$(ask "Choose [1/2/3]" "1")"
  case "$c" in
    1) TARGET="global" ;;
    2) TARGET="project" ;;
    3) TARGET="custom" ;;
    *) die "invalid choice: $c" ;;
  esac
  if [[ "$TARGET" == "custom" ]]; then
    OPENCODE_DIR="$(ask "Custom opencode config dir (agents/skills live under it)" "$OPENCODE_DIR")"
    GLOBAL_AGENT_DIR="$OPENCODE_DIR/agents"
    GLOBAL_SKILL_DIR="$OPENCODE_DIR/skills"
  fi
}

resolve_skills() {
  local available=("pufi-image" "pufi-anime")
  if [[ -z "$SKILLS" && $ASSUME_YES -eq 1 ]]; then
    SKILLS="all"
  fi
  if [[ -n "$SKILLS" ]]; then
    case "$SKILLS" in
      all) return ;;
      *)
        for s in "${available[@]}"; do [[ "$SKILLS" == "$s" ]] && return; done
        die "bad --skill: $SKILLS (all|${available[*]})"
        ;;
    esac
  fi
  echo "Which skills to deploy?"
  echo "  all          → ${available[*]}"
  for s in "${available[@]}"; do
    echo "  $s"
  done
  SKILLS="$(ask "Choose [all/${available[*]}]" "all")"
  case "$SKILLS" in
    all) ;;
    *)
      for s in "${available[@]}"; do [[ "$SKILLS" == "$s" ]] && return; done
      die "invalid skill choice: $SKILLS"
      ;;
  esac
}

resolve_persona() {
  if [[ -n "$PERSONA" ]]; then
    case "$PERSONA" in
      full|light) ;;
      *) die "bad --persona: $PERSONA (full|light)" ;;
    esac
  elif [[ "$EDITION" == "public" ]]; then
    PERSONA="light"
  elif [[ $ASSUME_YES -eq 1 ]]; then
    PERSONA="full"
  else
    echo "Persona:"
    echo "  full  → pufi-nsfw/pufi.md (complete private persona)  [private default]"
    echo "  light → pufi/pufi.md (suggestive/safe persona, for public)"
    PERSONA="$(ask "Choose [full/light]" "full")"
  fi
  if [[ "$PERSONA" == "full" && ! -f "$REPO_DIR/pufi-nsfw/pufi.md" ]]; then
    die "--persona full is not available in the public edition"
  fi
  case "$PERSONA" in
    full|light) ;;
    *) die "invalid persona: $PERSONA" ;;
  esac
}

persona_source() { # echo persona file path
  if [[ "$PERSONA" == "full" ]]; then
    echo "$REPO_DIR/pufi-nsfw/pufi.md"
  else
    echo "$REPO_DIR/pufi/pufi.md"
  fi
}

skill_source() { # skill_source <name> → echo source dir
  echo "$REPO_DIR/skills/$1"
}

agent_dir() {
  if [[ "$TARGET" == "project" ]]; then echo "$PROJECT_AGENT_DIR"; else echo "$GLOBAL_AGENT_DIR"; fi
}

skill_dir() {
  if [[ "$TARGET" == "project" ]]; then echo "$PROJECT_SKILL_DIR"; else echo "$GLOBAL_SKILL_DIR"; fi
}

# ---- opencode.json merge ---------------------------------------------------

merge_opencode_config() { # merge_opencode_config <config path>
  python3 - "$1" <<'PY'
import json, os, sys

path = sys.argv[1]
allows = {
    "~/.config/opencode/**": "allow",
    "~/.config/opencode/skills/pufi-image/**": "allow",
    "~/.config/opencode/skills/pufi-anime/**": "allow",
    "~/.config/pufi/**": "allow",
    "~/.local/share/pufi-image/**": "allow",
    "~/.local/share/pufi-anime/**": "allow",
}
if os.path.isfile(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"cannot parse {path}: {e}", file=sys.stderr)
        sys.exit(2)
else:
    data = {"$schema": "https://opencode.ai/config.json"}

data.setdefault("default_agent", "pufi")
perm = data.setdefault("permission", {}).setdefault("external_directory", {})
for key, value in allows.items():
    perm.setdefault(key, value)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
}

action_config() {
  # Auto-merge the workspace opencode.json for project/custom installs.
  local workspace=""
  case "$TARGET" in
    project) workspace="$REPO_DIR" ;;
    custom)
      [[ "$(basename "$OPENCODE_DIR")" == ".opencode" ]] && workspace="$(dirname "$OPENCODE_DIR")"
      ;;
  esac
  [[ -n "$workspace" ]] || return 0

  local cfg="$workspace/opencode.json" cfgc="$workspace/opencode.jsonc"
  if [[ ! -f "$cfg" && -f "$cfgc" ]]; then
    warn "found $cfgc — add \"default_agent\": \"pufi\" and permissions manually (JSONC is not auto-merged)"
    return 0
  fi
  if ! command -v python3 >/dev/null; then
    warn "python3 not found — add \"default_agent\": \"pufi\" and permissions to $cfg manually"
    return 0
  fi
  if out="$(merge_opencode_config "$cfg" 2>&1)"; then
    log "config  → $cfg"
  else
    warn "opencode.json merge failed: $out"
  fi
}

# ---- actions ---------------------------------------------------------------

action_doctor() {
  echo "=== Pufi deployment doctor ($EDITION edition) ==="
  echo "target              : ${TARGET:-global}"
  echo "opencode config dir : $OPENCODE_DIR"
  echo "python3             : $(command -v python3 || echo MISSING)"
  for f in "$(agent_dir)/pufi.md" "$(skill_dir)/pufi-image/SKILL.md" "$(skill_dir)/pufi-anime/SKILL.md"; do
    if [[ -f "$f" ]]; then
      echo "OK   $f"
    else
      echo "--   $f"
    fi
  done
  echo "--- env files ---"
  for e in "$PUFI_CONFIG_DIR/image.env" "$PUFI_CONFIG_DIR/anime.env"; do
    if [[ -f "$e" ]]; then
      echo "OK   $e ($(grep -cE '=' "$e") vars)"
    else
      echo "--   $e"
    fi
  done
}

action_uninstall() {
  local files=()
  for f in "$(agent_dir)/pufi.md" "$(skill_dir)/pufi-image" "$(skill_dir)/pufi-anime"; do
    [[ -e "$f" ]] && files+=("$f")
  done
  if [[ ${#files[@]} -eq 0 ]]; then
    log "nothing installed to remove."
    return
  fi
  echo "Will remove:"
  for f in "${files[@]}"; do echo "  $f"; done
  confirm "remove these" || { log "aborted."; exit 0; }
  if [[ $DRY_RUN -eq 1 ]]; then log "dry-run: nothing removed."; return; fi
  for f in "${files[@]}"; do rm -rf "$f"; done
  log "uninstalled."
}

action_setup_env() {
  mkdir -p "$PUFI_CONFIG_DIR"
  local which_skill
  which_skill="$(ask "Configure env for which skill? [pufi-image/pufi-anime]" "pufi-image")"
  local envfile="$PUFI_CONFIG_DIR/${which_skill#pufi-}.env"
  if [[ "$which_skill" == "pufi-image" ]]; then
    local url key model outdir
    url="$(ask "  PUFI_IMAGE_API_URL  (image API base URL)" "")"
    key="$(ask "  PUFI_IMAGE_API_KEY  (API key)" "")"
    model="$(ask "  PUFI_IMAGE_MODEL    (model)" "gpt-image-2")"
    outdir="$(ask "  PUFI_IMAGE_OUTPUT_DIR (output folder, blank = default)" "")"
    { echo "# pufi-image config (generated by install.sh)";
      [[ -n "$url" ]]    && echo "PUFI_IMAGE_API_URL=$url";
      [[ -n "$key" ]]    && echo "PUFI_IMAGE_API_KEY=$key";
      [[ -n "$model" ]]  && echo "PUFI_IMAGE_MODEL=$model";
      [[ -n "$outdir" ]] && echo "PUFI_IMAGE_OUTPUT_DIR=$outdir";
    } > "$envfile"
  elif [[ "$which_skill" == "pufi-anime" ]]; then
    local key base outdir
    key="$(ask "  LATENT_API_KEY    (Latent API key)" "")"
    base="$(ask "  LATENT_BASE_URL   (default https://latent.moe)" "https://latent.moe")"
    outdir="$(ask "  PUFI_ANIME_OUTPUT_DIR (output folder, blank = default)" "")"
    { echo "# pufi-anime config (generated by install.sh)";
      [[ -n "$key" ]]    && echo "LATENT_API_KEY=$key";
      [[ -n "$base" ]]   && echo "LATENT_BASE_URL=$base";
      [[ -n "$outdir" ]] && echo "PUFI_ANIME_OUTPUT_DIR=$outdir";
    } > "$envfile"
  else
    die "unknown skill: $which_skill"
  fi
  chmod 600 "$envfile"
  log "wrote $envfile"
}

action_smoke() {
  local py="$(command -v python3 || true)"
  [[ -n "$py" ]] || die "python3 not found"
  for skill in pufi-image pufi-anime; do
    local script
    case "$skill" in
      pufi-image) script="generate_image.py" ;;
      pufi-anime) script="generate.py" ;;
    esac
    local skill_path="$(skill_dir)/$skill"
    [[ -d "$skill_path/scripts" ]] || continue
    log "smoke: $skill --time"
    (cd "$skill_path" && python3 "scripts/$script" --time || true)
    log "smoke: $skill --prompt-only (dry)"
    (cd "$skill_path" && python3 "scripts/$script" \
      --prompt "A young anime catgirl with pale golden hair, sitting by a rainy window, warm mug, calm." \
      --prompt-only || true)
  done
}

action_install() {
  command -v rsync >/dev/null || die "rsync is required but not installed"
  resolve_target
  resolve_skills
  resolve_persona

  local agent_src; agent_src="$(persona_source)"
  local skill_names=()
  if [[ "$SKILLS" == "all" ]]; then
    skill_names=("pufi-image" "pufi-anime")
  else
    skill_names=("$SKILLS")
  fi

  local tgt_agent tgt_skills
  tgt_agent="$(agent_dir)"
  tgt_skills="$(skill_dir)"

  local rsync_excludes=(--exclude 'outputs/' --exclude '__pycache__/' --exclude '*.pyc')
  if [[ "$EDITION" == "public" ]]; then
    # raw Danbooru tag data stays out of the public edition
    rsync_excludes+=(--exclude 'tags/tags.jsonl' --exclude 'tags/groups.json')
  fi

  echo
  echo "=== Install plan ($EDITION edition) ==="
  echo "  target   : $TARGET → $OPENCODE_DIR"
  echo "  persona  : $PERSONA ($agent_src)"
  echo "             → $tgt_agent/pufi.md"
  for s in "${skill_names[@]}"; do
    echo "  skill    : $s ($(skill_source "$s"))"
    echo "             → $tgt_skills/$s"
  done
  if [[ "$TARGET" == "project" || "$TARGET" == "custom" ]]; then
    echo "  config   : auto-merge default_agent/permissions into the workspace opencode.json"
  fi
  echo
  confirm "install to the paths above" || { log "aborted."; exit 0; }
  if [[ $DRY_RUN -eq 1 ]]; then log "dry-run: nothing written."; return; fi

  mkdir -p "$tgt_agent" "$tgt_skills"
  cp "$agent_src" "$tgt_agent/pufi.md"
  log "agent   → $tgt_agent/pufi.md"

  for s in "${skill_names[@]}"; do
    local src="$(skill_source "$s")"
    [[ -d "$src" ]] || die "skill source not found: $src"
    rsync -a --delete "${rsync_excludes[@]}" "$src/" "$tgt_skills/$s/"
    log "skill   → $tgt_skills/$s"
  done

  action_config

  echo
  log "done. Restart opencode for the changes to take effect."
  echo "  Configure API keys:  ./install.sh --setup-env"
  echo "  Verify:              ./install.sh doctor / --smoke"
  if [[ "$TARGET" == "global" ]]; then
    echo "  Workspace config:    per-project opencode.json may still need \"default_agent\" + permissions"
  fi
}

# ---- main ------------------------------------------------------------------

# --opencode-dir makes custom targets usable by every action (install/doctor/smoke/uninstall).
if [[ -n "$CUSTOM_DIR" ]]; then
  case "${TARGET:-custom}" in
    custom) ;;
    *) die "--opencode-dir is only valid with --target custom (got: $TARGET)" ;;
  esac
  TARGET="custom"
  OPENCODE_DIR="$CUSTOM_DIR"
  GLOBAL_AGENT_DIR="$OPENCODE_DIR/agents"
  GLOBAL_SKILL_DIR="$OPENCODE_DIR/skills"
elif [[ "$TARGET" == "custom" && "$ACTION" != "install" ]]; then
  die "--target custom requires --opencode-dir for $ACTION"
fi

case "$ACTION" in
  install)    action_install ;;
  setup_env)  action_setup_env ;;
  smoke)      action_smoke ;;
  doctor)     action_doctor ;;
  uninstall)  action_uninstall ;;
esac
