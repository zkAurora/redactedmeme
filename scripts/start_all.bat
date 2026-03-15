@echo off
REM Minimal mono-repo launcher for SWARM: gateway + TS swarm-core
REM Usage: start_all.bat
setlocal
echo Starting gateway and swarm-core in parallel...
start "gateway" cmd /c "bun run index.js" 
start "swarm-core" cmd /c "bun run ts-server" 
echo Started. Use Ctrl+C to stop.
pause
