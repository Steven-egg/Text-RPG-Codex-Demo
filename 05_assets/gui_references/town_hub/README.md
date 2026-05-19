# Town Hub GUI References

用途：暫存 Town Hub 的 visual reference、user mockup 與 generated candidate。此資料夾只做 GUI planning / review 參考，不代表正式 runtime asset path。

## 邊界

- 這裡的圖片是 reference / candidate，不是正式 runtime asset。
- 不代表已啟動正式 asset pipeline。
- 不應被 `03_engine` 或 runtime 直接引用。
- 不應把圖片內 icon、建築或 UI chrome 視為 gameplay 資料來源。
- 所有 title、facility label、resource value、badge、guidance 與 action label 都必須由 render layer 動態輸出。

## Files

### `town_hub_visual_reference_v1_user_mockup.png`

使用者提供的 Town Hub visual reference / user mockup。

狀態：

- `user_reference`
- `reviewed_candidate`
- `accepted_direction`

用途：

- 驗證 Town Hub 場景式 facility hub 方向。
- 驗證 `facility_nodes` 可由建築入口承接。
- 提供早期 visual direction，不作 runtime 使用。

### `town_hub_visual_mockup_candidate_v1_001.png`

AI 生成的 Town Hub visual mockup candidate。

狀態：

- `generated_candidate`
- `reviewed_candidate`
- `accepted_direction`

用途：

- 作為 Town Hub V1 的 visual mockup reference candidate。
- 驗證 safe areas、facility entrance coverage、resource strip、town guidance、badge slots 與 dynamic text safety。
- 支援後續 programmatic layout planning。

來源：

```text
C:\Users\user\.codex\generated_images\019e3bba-e6c2-78f0-97e2-59bb0436eaa8\ig_0978a4b347977fd9016a0b9da7c12c8191aa682dbfa91fc510.png
```

相關文件：

- `01_content/gui-town-hub-visual-mockup-prompt-draft.md`
- `01_content/gui-town-hub-visual-mockup-prompt-review-v1.md`
- `01_content/gui-town-hub-visual-mockup-candidate-review-v1.md`
- `01_content/gui-town-hub-facility-node-mapping-v1.md`
- `01_content/gui-town-hub-programmatic-layout-plan-v1.md`

