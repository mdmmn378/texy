watch_memory() {
  target="$1"
  if [ -z "$target" ]; then
    echo "Usage: watch_memory <process_name>"
    return 1
  fi

  watch -n 2 "ps -aux | grep \"$target\" | grep -v grep | awk '{print \$2}' | xargs -r -I % vmrss %"
}

watch_memory "$1"