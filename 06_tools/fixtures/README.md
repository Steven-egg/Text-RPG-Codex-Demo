# 玩家測試存檔

`fire-cleared-ice-ready-save.json` 是獨立測試檔：Fire 主線與三個必要 Boss
已完成、火之聖印已安置、Ice 已開放但尚未進行。角色為 Lv11 劍士，裝備四件
合法的精良品質 equipment instances。

從 repository 根目錄執行下列命令；若已有 `save.json`，第一行會先保留它，
不會覆寫：

```powershell
if (Test-Path .\save.player-backup.json) { throw '既有 save.player-backup.json，請先改名或移走。' }
if (Test-Path .\save.json) { Move-Item .\save.json .\save.player-backup.json }
Copy-Item .\06_tools\fixtures\fire-cleared-ice-ready-save.json .\save.json
```

測試後若要還原原存檔：

```powershell
if (Test-Path .\save.player-backup.json) { Move-Item -Force .\save.player-backup.json .\save.json }
```
