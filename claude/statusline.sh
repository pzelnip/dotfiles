#!/usr/bin/env bash
# Claude Code status line.
# Receives session state as JSON on stdin; prints a single line to stdout.
# See the field reference below for everything available on the input object.

input=$(cat)

model=$(printf '%s' "$input" | jq -r '.model.display_name // "unknown"')
current_dir=$(printf '%s' "$input" | jq -r '.workspace.current_dir // .cwd // "?"')
project_dir=$(printf '%s' "$input" | jq -r '.workspace.project_dir // "?"')
session_id=$(printf '%s' "$input" | jq -r '.session_id // "?"')
cost=$(printf '%s' "$input" | jq -r '.cost.total_cost_usd // 0 | "$" + (. * 10000 | round / 10000 | tostring)')

# ANSI colors (standard palette — tracks the terminal theme).
c_model=$'\033[1;36m'   # bold cyan
c_dir=$'\033[94m'       # bright blue (plain blue is too dark on black backgrounds)
c_proj=$'\033[32m'      # green
c_sess=$'\033[35m'      # magenta
c_cost=$'\033[33m'      # yellow
dim=$'\033[90m'         # bright black — labels & separators
reset=$'\033[0m'

sep="${dim} | ${reset}"

out="${c_model}${model}${reset}"
out+="${sep}${dim}cwd: ${reset}${c_dir}${current_dir}${reset}"
out+="${sep}${dim}proj: ${reset}${c_proj}${project_dir}${reset}"
out+="${sep}${dim}session: ${reset}${c_sess}${session_id}${reset}"
out+="${sep}${dim}Cost: ${reset}${c_cost}${cost}${reset}"

printf '%s' "$out"
