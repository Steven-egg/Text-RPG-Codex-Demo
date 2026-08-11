# 測試存檔 profiles

Fixtures 放在 `saves/`；每個 profile 是可提交、不可直接修改的起始狀態。執行
runtime bridge 時，遊戲會把 fixture 複製到被 Git 忽略的 `.test-saves/`，後續
存檔只寫入該副本，不會讀寫你的 `save.json`。

目前提供：

- `ice-entry.json`：Fire 主線與三個必要 Boss 已完成、火之聖印已安置、Ice 已開放
  但尚未進行。角色為 Lv11 劍士，裝備四件合法的精良品質 equipment instances。

從 repository 根目錄啟動 Ice 入口測試：

```powershell
$mazePython = 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $mazePython -B .\06_tools\gui_runtime_bridge.py --test-profile ice-entry
```

第一次會建立 `.test-saves/ice-entry.json`；之後會保留這份測試進度。若要從 fixture
重來，加上 `--reset-test-profile`：

```powershell
& $mazePython -B .\06_tools\gui_runtime_bridge.py --test-profile ice-entry --reset-test-profile
```

CLI 也可直接選用專案內的獨立存檔路徑，例如：

```powershell
& $mazePython .\element_maze.py --save-path .test-saves\ice-entry.json
```
