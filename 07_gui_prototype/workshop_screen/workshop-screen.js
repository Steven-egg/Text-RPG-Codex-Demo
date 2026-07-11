/**
 * ELM FORGE - Workshop Screen Prototype Logic
 * Programmatic GUI -> Asset-driven. Built purely on static fixtures.
 */
import { applyFacilityBackground } from "../shared/facility-backgrounds.js";
import { runtimeClient } from "../shared/runtime-client.js";

// 全域狀態變數
let currentFixtureData = null;
let currentTab = 'weapon'; // 'weapon', 'armor', 'upgrade', 'owned'
let selectedItemId = null;
let uiActionLogs = [];

const workshopBackgroundByRegion = {
  fire: {
    "--facility-background-image": "./assets/workshop-background.jpg",
    "--facility-background-image-2": "./assets/workshop-background-02.jpg",
  },
  ice: {
    "--facility-background-image": "./assets/ice-weapon-workshop-with-gray-candidate-v02.png",
    "--facility-background-image-2": "./assets/ice-armor-workshop-with-brin-cropped-candidate-v03.png",
  },
  earth: {
    "--facility-background-image": "./assets/earth-weapon-workshop-background-with-gray-cropped-candidate-v02.png",
    "--facility-background-image-2": "./assets/earth-armor-workshop-background-with-bryn-cropped-candidate-v01.png",
  },
  thunder: {
    "--facility-background-image": "./assets/thunder-weapon-workshop-background-with-gray-candidate-v01.png",
    "--facility-background-image-2": "./assets/thunder-armor-workshop-background-with-bryn-candidate-v01.png",
  },
  final: {
    "--facility-background-image": "./assets/final-weapon-workshop-with-gray-candidate-v01.png",
    "--facility-background-image-2": "./assets/final-armor-workshop-with-bryn-candidate-v01.png",
  },
};

// DOM 元素引用
const playerNameEl = document.getElementById('player-name');
const playerJobEl = document.getElementById('player-job');
const playerGoldEl = document.getElementById('player-gold');
const fixtureSelect = document.getElementById('fixture-select');
const itemListContainer = document.getElementById('item-list-container');
const itemDetailView = document.getElementById('item-detail-view');
const requirementBox = document.getElementById('requirement-box');
const itemRequirementView = document.getElementById('item-requirement-view');
const npcRoleEl = document.getElementById('npc-role');
const npcNameEl = document.getElementById('npc-name');
const npcVisualEl = document.getElementById('npc-visual');
const npcDialogEl = document.getElementById('npc-dialog');
const npcStage = document.getElementById('npc-stage');
const feedbackBar = document.getElementById('feedback-bar');
const primaryActionBtn = document.getElementById('primary-action');
const backToTownBtn = document.getElementById('back-to-town');
const debugToggle = document.getElementById('debug-toggle');
const debugContainer = document.querySelector('.debug-container');
const debugLogView = document.getElementById('debug-log-view');

// Tabs 按鈕
const tabButtons = document.querySelectorAll('.tab-btn');

// 初始化載入
document.addEventListener('DOMContentLoaded', () => {
  if (runtimeClient.isLiveMode()) {
    const selectorContainer = document.querySelector('.fixture-selector-container');
    if (selectorContainer) {
      selectorContainer.style.display = 'none';
    }
  }

  // 1. 綁定 Fixture Selector
  fixtureSelect.addEventListener('change', (e) => {
    loadFixture(e.target.value);
  });

  // 2. 綁定 Tabs 切換
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-category');
      switchTab(category);
    });
  });

  // 3. 綁定返回按鈕
  backToTownBtn.addEventListener('click', () => {
    logUIAction('back_to_town_hub', {});
    renderFeedback("系統", "正在返回邊境城鎮艾爾姆...");

    if (runtimeClient.isLiveMode()) {
      runtimeClient.dispatchAction("workshop_screen", "back_to_town_hub", {})
        .then((result) => {
          window.location.href = runtimeClient.nextRoute(result, '../town_hub/index.html');
        })
        .catch((err) => {
          console.error(err);
          window.location.href = '../town_hub/index.html?mode=live';
        });
    } else {
      window.location.href = '../town_hub/index.html';
    }
  });

  // 4. 綁定除錯面板 toggle
  debugToggle.addEventListener('click', () => {
    debugContainer.classList.toggle('expanded');
  });

  // 5. 綁定主要按鈕
  primaryActionBtn.addEventListener('click', () => {
    handlePrimaryAction();
  });

  // 預設載入首個 Fixture
  loadFixture('workshop-default.json');
});

/**
 * 載入指定 Fixture
 */
function loadFixture(fileName) {
  if (runtimeClient.isLiveMode()) {
    loadLiveScreen();
    return;
  }
  loadStaticFallback(fileName);
}

async function loadLiveScreen() {
  try {
    const model = await runtimeClient.getScreen("workshop_screen");
    currentFixtureData = model;
    logUIAction('live_screen_loaded', {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "workshop_screen" }
    });

    // 更新 Header
    playerNameEl.textContent = `冒險者: ${model.player.name}`;
    playerJobEl.textContent = `職業: ${model.player.job} (Lv${model.player.level})`;
    playerGoldEl.textContent = `${model.player.gold}G`;

    // 更新分類計數
    updateCounts();

    // 切換並渲染當前 Tab
    switchTab(currentTab, true);

    if (model.feedback_message) {
      renderFeedback(model.feedback_message.speaker ?? (model.npc?.name ?? "葛雷"), model.feedback_message.text, model.feedback_message.tone);
    } else {
      renderFeedback(model.npc?.name ?? "葛雷", "工坊設備已就緒，請選擇項目。");
    }
  } catch (error) {
    console.error(error);
    const reason = runtimeClient.errorMessage(error);
    logUIAction('live_bridge_unavailable', {
      action_id: "live_bridge_unavailable",
      payload: { reason },
      source: "live_loader",
      dispatched: false,
      reason: "fallback_to_fixture"
    });
    renderFeedback("系統", `Live 連線失敗，載入靜態 Fixture: ${reason}`, 'danger');
    loadStaticFallback('workshop-default.json');
  }
}

function loadStaticFallback(fileName) {
  const url = `./fixtures/${fileName}`;
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error(`無法載入 Fixture: ${fileName}`);
      }
      return response.json();
    })
    .then(data => {
      currentFixtureData = data;
      logUIAction('load_fixture', { file: fileName, player: data.player.name, job: data.player.job });
      
      // 更新 Header
      playerNameEl.textContent = `冒險者: ${data.player.name}`;
      playerJobEl.textContent = `職業: ${data.player.job} (Lv${data.player.level})`;
      playerGoldEl.textContent = `${data.player.gold}G`;

      // 更新分類計數
      updateCounts();

      // 切換並渲染當前 Tab
      switchTab(currentTab, true);
      
      renderFeedback("葛雷", "工坊設備已就緒，請選擇項目。");
    })
    .catch(err => {
      console.error(err);
      renderFeedback("系統", `讀取 Fixture 失敗: ${err.message}`, 'danger');
    });
}

/**
 * 更新 Tab 上面的計數器
 */
function updateCounts() {
  if (!currentFixtureData) return;

  const weaponCount = currentFixtureData.weapons.length;
  const armorCount = currentFixtureData.armors.length;
  const upgradeCount = currentFixtureData.upgrades.length;
  
  // 計算已擁有/已裝備的數量 (只統計玩家 inventory 內裝備 + 目前 equipped 裝備)
  const ownedItems = getOwnedItemsList();
  let ownedCount = 0;
  ownedItems.forEach(item => {
    ownedCount += item.count;
  });

  document.getElementById('count-weapon').textContent = weaponCount;
  document.getElementById('count-armor').textContent = armorCount;
  document.getElementById('count-upgrade').textContent = upgradeCount;
  document.getElementById('count-owned').textContent = ownedCount;
}

/**
 * 切換標籤頁
 */
function switchTab(category, forceRefresh = false) {
  if (currentTab === category && !forceRefresh) return;

  currentTab = category;
  applyFacilityBackground({
    model: currentFixtureData,
    shell: document.body,
    backgrounds: workshopBackgroundByRegion,
  });
  logUIAction('select_tab', { tab_id: category });

  // 更新 Tab 按鈕樣式
  tabButtons.forEach(btn => {
    if (btn.getAttribute('data-category') === category) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  // 切換 NPC 主題視覺
  updateNPCTheme(category);

  // 渲染列表
  renderList();
}

/**
 * 依據分類切換 NPC 及對應樣式
 */
function updateNPCTheme(category, selectedItem = null) {
  // 依據類別或當前選取品項判定是否為武器相關
  let isWeaponRelated = true;

  if (category === 'weapon') {
    isWeaponRelated = true;
  } else if (category === 'armor') {
    isWeaponRelated = false;
  } else if (category === 'upgrade') {
    if (selectedItem) {
      const baseId = selectedItem.base_item || '';
      if (baseId.startsWith('weapon_')) {
        isWeaponRelated = true;
      } else {
        isWeaponRelated = false;
      }
    } else {
      isWeaponRelated = true;
    }
  } else if (category === 'owned') {
    if (selectedItem) {
      const slot = selectedItem.slot || '';
      if (slot === 'weapon') {
        isWeaponRelated = true;
      } else {
        isWeaponRelated = false;
      }
    } else {
      isWeaponRelated = true;
    }
  }

  if (isWeaponRelated) {
    // 鐵刃工坊葛雷
    npcRoleEl.textContent = '武器鍛造大師';
    npcNameEl.textContent = '葛雷';
    npcStage.className = 'right-column panel-border grey-forge';
    document.querySelector('.npc-silhouette-area').className = 'npc-silhouette-area grey-forge';
    
    if (category === 'upgrade') {
      npcDialogEl.textContent = '「想讓你的鐵劍更鋒利嗎？帶上素材與金幣，我來搞定。」';
    } else {
      npcDialogEl.textContent = '「最好的防禦就是進攻。挑一把趁手的傢伙，冒險者。」';
    }
  } else {
    // 堅甲工坊布琳
    npcRoleEl.textContent = '防具裁作師';
    npcNameEl.textContent = '布琳';
    npcStage.className = 'right-column panel-border brin-armor';
    document.querySelector('.npc-silhouette-area').className = 'npc-silhouette-area brin-armor';
    
    if (category === 'upgrade') {
      npcDialogEl.textContent = '「防護是探險的基石。穿上我強化過的甲冑，焦石礦坑也傷不到你。」';
    } else {
      // owned 或 armor 情況
      npcDialogEl.textContent = '「耐用、實惠，我的防具每一件都經得起邊境魔物的考驗。」';
    }
  }
}

/**
 * 渲染品項列表
 */
function renderList() {
  itemListContainer.innerHTML = '';
  if (!currentFixtureData) return;

  let listItems = [];

  if (currentTab === 'weapon') {
    listItems = currentFixtureData.weapons;
  } else if (currentTab === 'armor') {
    listItems = currentFixtureData.armors;
  } else if (currentTab === 'upgrade') {
    listItems = currentFixtureData.upgrades;
  } else if (currentTab === 'owned') {
    listItems = getOwnedItemsList();
  }

  if (listItems.length === 0) {
    itemListContainer.innerHTML = '<p class="placeholder-text" style="padding: 20px;">無此項目</p>';
    selectedItemId = null;
    updateDetailView(null);
    return;
  }

  listItems.forEach((item, index) => {
    const row = document.createElement('div');
    row.className = 'list-item-row';
    row.setAttribute('data-id', item.id);

    const checkRes = checkRequirements(item);
    
    // 左側：圓點與名字
    const leftZone = document.createElement('div');
    leftZone.className = 'item-left';
    
    const dot = document.createElement('span');
    dot.className = `item-visual-indicator ${currentTab}-dot`;
    leftZone.appendChild(dot);

    const name = document.createElement('span');
    name.className = 'item-name';
    if (currentTab === 'owned' && item.equippedSlot) {
      name.textContent = `${item.name}（已裝備）`;
    } else {
      name.textContent = item.name;
    }
    leftZone.appendChild(name);

    row.appendChild(leftZone);

    // 右側：Badge 或 價格
    const rightZone = document.createElement('div');
    rightZone.className = 'item-right';

    if (currentTab === 'owned') {
      const badge = document.createElement('span');
      badge.className = 'item-badge can-deal';
      badge.textContent = `x${item.count}`;
      rightZone.appendChild(badge);
    } else {
      // 顯示狀態 Badge
      const badge = document.createElement('span');
      badge.className = 'item-badge';
      
      if (currentTab === 'upgrade') {
        const isLocked = isRecipeLocked(item);
        if (isLocked) {
          badge.textContent = '鎖定';
          badge.className += ' locked';
        } else if (!checkRes.satisfied) {
          badge.textContent = checkRes.reasonText;
          badge.className += ' blocked';
        } else {
          badge.textContent = '可強化';
          badge.className += ' can-deal';
        }
      } else {
        // 購買裝備
        if (!checkRes.satisfied) {
          badge.textContent = checkRes.reasonText;
          badge.className += ' blocked';
        } else {
          badge.textContent = '可購買';
          badge.className += ' can-deal';
        }
      }
      rightZone.appendChild(badge);

      // 價格
      const price = document.createElement('span');
      price.className = 'item-price-label';
      price.textContent = `${item.price || item.gold}G`;
      rightZone.appendChild(price);
    }

    row.appendChild(rightZone);

    // 點擊事件
    row.addEventListener('click', () => {
      document.querySelectorAll('.list-item-row').forEach(r => r.classList.remove('selected'));
      row.classList.add('selected');
      selectedItemId = item.id;
      
      if (currentTab === 'upgrade') {
        logUIAction('select_recipe', { recipe_id: item.id });
      } else {
        logUIAction('select_item', { item_id: item.id });
      }
      
      updateDetailView(item);
    });

    itemListContainer.appendChild(row);

    // 預設選中第一個項目
    if (index === 0) {
      row.classList.add('selected');
      selectedItemId = item.id;
      updateDetailView(item);
    }
  });
}

/**
 * 取得玩家目前擁有的裝備清單
 */
function getOwnedItemsList() {
  const map = new Map();
  const player = currentFixtureData.player;

  // 1. 已裝備項目
  Object.keys(player.equipment).forEach(slot => {
    const itemId = player.equipment[slot];
    if (!itemId) return;
    const itemDetail = findItemInFixtures(itemId);
    if (itemDetail) {
      if (map.has(itemId)) {
        const existing = map.get(itemId);
        existing.count += 1;
        existing.equippedSlot = slot;
      } else {
        map.set(itemId, {
          ...itemDetail,
          count: 1,
          equippedSlot: slot
        });
      }
    }
  });

  // 2. 背包中的武器防具飾品
  Object.keys(player.inventory).forEach(itemId => {
    if (itemId.startsWith('weapon_') || itemId.startsWith('armor_') || itemId.startsWith('acc_') || itemId.startsWith('special_')) {
      const qty = player.inventory[itemId];
      if (qty > 0) {
        const itemDetail = findItemInFixtures(itemId);
        if (itemDetail) {
          if (map.has(itemId)) {
            const existing = map.get(itemId);
            existing.count += qty;
          } else {
            map.set(itemId, {
              ...itemDetail,
              count: qty,
              equippedSlot: null
            });
          }
        }
      }
    }
  });

  return Array.from(map.values());
}

/**
 * 從 Fixtures 資料中檢索裝備屬性
 */
function findItemInFixtures(itemId) {
  if (currentFixtureData && currentFixtureData.weapons_details && currentFixtureData.weapons_details[itemId]) {
    return currentFixtureData.weapons_details[itemId];
  }

  const inWeapons = currentFixtureData.weapons.find(w => w.id === itemId);
  if (inWeapons) return inWeapons;

  const inArmors = currentFixtureData.armors.find(a => a.id === itemId);
  if (inArmors) return inArmors;

  // 強化版本的屬性或未列出裝備回落防呆
  if (itemId === 'weapon_iron_sword_plus_1') {
    return { id: itemId, name: '鐵劍 +1', slot: 'weapon', subtype: '強化劍', price: 0, jobs: ['劍士'], stats: { attack: 18 }, desc: '攻擊力明顯提升的強化鐵劍。' };
  }
  if (itemId === 'armor_leather_armor_plus_1') {
    return { id: itemId, name: '皮甲 +1', slot: 'body', subtype: '強化甲', price: 0, jobs: ['劍士', '盜賊', '牧師'], stats: { defense: 15, agility: -1 }, desc: '強化後的皮甲。' };
  }
  if (itemId === 'acc_lucky_charm') {
    return { id: itemId, name: '幸運小符', slot: 'accessory', subtype: '飾品', price: 160, jobs: ['劍士', '法師', '盜賊', '牧師'], stats: { rare_drop: 3 }, desc: '稀有素材掉落機率 +3%。' };
  }
  if (itemId === 'acc_warm_stone') {
    return { id: itemId, name: '暖石墜', slot: 'accessory', subtype: '飾品', price: 260, jobs: ['劍士', '法師', '盜賊', '牧師'], stats: { fire_resist: 10 }, desc: '火傷害 -10%。' };
  }

  return null;
}

/**
 * 判斷強化配方是否被鎖定
 */
function isRecipeLocked(recipe) {
  if (!recipe.unlock_quest) return false;
  return !currentFixtureData.player.completed_quests.includes(recipe.unlock_quest);
}

/**
 * 檢查金幣、基底、素材是否滿足
 */
function checkRequirements(item) {
  const player = currentFixtureData.player;

  if (currentTab === 'owned') {
    return { satisfied: true, reasonText: '已擁有' };
  }

  // 1. 檢查配方解鎖（針對強化）
  if (currentTab === 'upgrade') {
    if (isRecipeLocked(item)) {
      return { satisfied: false, reasonText: '未解鎖', disabledReason: 'recipe_locked' };
    }
  }

  // 2. 檢查職業限制
  const currentJob = player.job;
  if (currentTab !== 'upgrade' && item.jobs && !item.jobs.includes(currentJob)) {
    // 配方輸出裝備的職業可用性
    return { satisfied: false, reasonText: '職業不合', disabledReason: 'job_incompatible' };
  }

  // 3. 檢查金幣
  const price = item.price || item.gold;
  if (player.gold < price) {
    return { satisfied: false, reasonText: '錢不足', disabledReason: 'gold_deficient' };
  }

  // 4. 針對強化，額外檢查基底裝備與素材
  if (currentTab === 'upgrade') {
    // A. 檢查基底裝備 (在背包或已裝備算擁有)
    const baseId = item.base_item;
    const isEquipped = Object.values(player.equipment).includes(baseId);
    const inInventory = (player.inventory[baseId] || 0) > 0;
    if (!isEquipped && !inInventory) {
      return { satisfied: false, reasonText: '缺基底', disabledReason: 'missing_base_item' };
    }

    // B. 檢查素材消耗
    const mats = item.materials;
    let matsSatisfied = true;
    Object.keys(mats).forEach(matId => {
      const reqQty = mats[matId].required;
      const playerQty = player.inventory[matId] || 0;
      if (playerQty < reqQty) {
        matsSatisfied = false;
      }
    });

    if (!matsSatisfied) {
      return { satisfied: false, reasonText: '缺素材', disabledReason: 'materials_deficient' };
    }
  }

  return { satisfied: true, reasonText: '可交易' };
}

/**
 * 更新詳情面板與材料需求面板
 */
function updateDetailView(item) {
  if (!item) {
    itemDetailView.innerHTML = '<p class="placeholder-text">請選擇左側的品項查看詳情</p>';
    itemRequirementView.innerHTML = '<p class="placeholder-text">請選擇左側品項以確認交易需求</p>';
    setPrimaryActionText('選擇項目', true);
    return;
  }

  // 依據目前選中項目的類型，動態更新 NPC 的稱號、提示語與右側視覺主題
  updateNPCTheme(currentTab, item);

  const player = currentFixtureData.player;

  // 1. 渲染詳情面板
  let statsHtml = '';
  if (item.stats) {
    Object.keys(item.stats).forEach(statKey => {
      let label = statKey;
      if (statKey === 'attack') label = '物理攻擊力';
      if (statKey === 'magic_attack') label = '魔法攻擊力';
      if (statKey === 'defense') label = '物理防禦力';
      if (statKey === 'agility') label = '敏捷';
      if (statKey === 'crit') label = '暴擊率';
      if (statKey === 'fire_resist') label = '火屬性抗性';
      if (statKey === 'rare_drop') label = '稀有掉落率';
      if (statKey === 'trap_evasion') label = '陷阱迴避率';

      const val = item.stats[statKey];
      const sign = val > 0 ? `+${val}` : `${val}`;
      const suffix = (statKey === 'crit' || statKey === 'fire_resist' || statKey === 'rare_drop' || statKey === 'trap_evasion') ? '%' : '';
      statsHtml += `<span class="stat-tag"><span class="stat-label">${label}</span><span class="stat-value">${sign}${suffix}</span></span>`;
    });
  }

  let jobBadgesHtml = '';
  // 強化配方讀取 output 屬性
  const jobsAllowed = item.jobs || ['劍士', '盜賊', '牧師']; // 防呆
  const allJobs = ['劍士', '法師', '盜賊', '牧師'];
  allJobs.forEach(jobName => {
    let className = 'job-tag incompatible';
    if (jobsAllowed.includes(jobName)) {
      className = (jobName === player.job) ? 'job-tag current-active' : 'job-tag compatible';
    }
    jobBadgesHtml += `<span class="${className}">${jobName}</span>`;
  });

  const slotLabel = item.slot ? item.slot.toUpperCase() : (currentTab === 'upgrade' ? 'UPGRADE' : 'EQUIPMENT');
  const itemType = item.subtype || (currentTab === 'upgrade' ? '裝備強化' : '裝備');

  itemDetailView.innerHTML = `
    <div class="detail-grid">
      <div class="detail-row-header">
        <h2 class="detail-main-name">${item.name}</h2>
        <span class="detail-subtitle-type">${itemType}</span>
      </div>
      <div class="detail-desc-card">
        ${item.desc}
      </div>
      <h3 style="font-size: 11px; color: var(--gold-bright); font-weight: 800; margin-top: 5px;">屬性增益</h3>
      <div class="detail-stats-deck">
        ${statsHtml || '<span class="stat-tag"><span class="stat-label">無屬性增益</span></span>'}
      </div>
      <div class="job-compatibility-panel">
        <span class="job-compatibility-title">可用職業限制</span>
        <div class="job-badges-deck">
          ${jobBadgesHtml}
        </div>
      </div>
    </div>
  `;

  document.getElementById('detail-slot').textContent = slotLabel;

  // 2. 渲染需求與消耗面板
  renderRequirementsView(item);
}

/**
 * 渲染需求與消耗面板 (條狀)
 */
function renderRequirementsView(item) {
  const player = currentFixtureData.player;
  const checkRes = checkRequirements(item);
  let reqsHtml = '';

  if (currentTab === 'owned') {
    const currentJob = player.job;
    const jobCompatible = !item.jobs || item.jobs.includes(currentJob);

    if (item.equippedSlot) {
      itemRequirementView.innerHTML = `
        <div style="text-align: center; margin: auto;">
          <p style="font-size: 13px; color: var(--success-color); font-weight: bold; margin-bottom: 5px;">目前已裝備此裝備</p>
          <p style="font-size: 11px; color: var(--text-muted);">正在裝備欄位 [${item.equippedSlot.toUpperCase()}] 中發揮效果。</p>
        </div>
      `;
      setPrimaryActionText('裝備中', true);
      primaryActionBtn.removeAttribute('data-disabled-reason');
    } else if (!jobCompatible) {
      itemRequirementView.innerHTML = `
        <div style="text-align: center; margin: auto;">
          <p style="font-size: 13px; color: var(--danger-color); font-weight: bold; margin-bottom: 5px;">職業限制，無法裝備</p>
          <p style="font-size: 11px; color: var(--text-muted);">目前職業 [${currentJob}] 無法裝備此裝備。</p>
        </div>
      `;
      setPrimaryActionText('裝備此裝備', true);
      primaryActionBtn.setAttribute('data-disabled-reason', 'job_incompatible');
    } else {
      itemRequirementView.innerHTML = `
        <div style="text-align: center; margin: auto;">
          <p style="font-size: 13px; color: var(--info-blue); font-weight: bold; margin-bottom: 5px;">此裝備目前未裝備</p>
          <p style="font-size: 11px; color: var(--text-muted);">點擊按鈕將其裝備至冒險者的對應插槽。</p>
        </div>
      `;
      setPrimaryActionText('裝備此裝備', false);
      primaryActionBtn.removeAttribute('data-disabled-reason');
    }
    return;
  }

  // 1. 金幣需求
  const cost = item.price || item.gold;
  const goldSatisfied = player.gold >= cost;
  reqsHtml += `
    <div class="req-strip-row">
      <div class="req-name-zone">
        <span class="req-icon-dot gold-dot"></span>
        <span class="req-label">費用金幣 (Gold)</span>
      </div>
      <div class="req-val-zone">
        <span class="req-fraction ${goldSatisfied ? 'satisfied' : 'deficient'}">${player.gold}G / ${cost}G</span>
        <span class="req-status-icon ${goldSatisfied ? 'satisfied' : 'deficient'}">${goldSatisfied ? '✓' : '✗'}</span>
      </div>
    </div>
  `;

  // 2. 強化配方的解鎖/基底/素材需求
  if (currentTab === 'upgrade') {
    // A. 解鎖任務
    if (item.unlock_quest) {
      const questUnlocked = player.completed_quests.includes(item.unlock_quest);
      reqsHtml += `
        <div class="req-strip-row">
          <div class="req-name-zone">
            <span class="req-icon-dot base-dot"></span>
            <span class="req-label">解鎖任務: 洞窟採集</span>
          </div>
          <div class="req-val-zone">
            <span class="req-fraction ${questUnlocked ? 'satisfied' : 'deficient'}">${questUnlocked ? '已完成' : '未解鎖'}</span>
            <span class="req-status-icon ${questUnlocked ? 'satisfied' : 'deficient'}">${questUnlocked ? '✓' : '✗'}</span>
          </div>
        </div>
      `;
    }

    // B. 基底裝備
    const baseId = item.base_item;
    const isEquipped = Object.values(player.equipment).includes(baseId);
    const inInventory = (player.inventory[baseId] || 0) > 0;
    const hasBase = isEquipped || inInventory;
    const baseLocationText = isEquipped ? '已裝備' : (inInventory ? '背包持有' : '無');
    
    reqsHtml += `
      <div class="req-strip-row">
        <div class="req-name-zone">
          <span class="req-icon-dot base-dot"></span>
          <span class="req-label">需基底裝備: [${item.base_name}]</span>
        </div>
        <div class="req-val-zone">
          <span class="req-fraction ${hasBase ? 'satisfied' : 'deficient'}">${baseLocationText} (1/1)</span>
          <span class="req-status-icon ${hasBase ? 'satisfied' : 'deficient'}">${hasBase ? '✓' : '✗'}</span>
        </div>
      </div>
    `;

    // C. 素材需求
    const mats = item.materials;
    Object.keys(mats).forEach(matId => {
      const mat = mats[matId];
      const playerQty = player.inventory[matId] || 0;
      const isMatSatisfied = playerQty >= mat.required;

      reqsHtml += `
        <div class="req-strip-row">
          <div class="req-name-zone">
            <span class="req-icon-dot material-dot"></span>
            <span class="req-label">消耗素材: ${mat.name}</span>
          </div>
          <div class="req-val-zone">
            <span class="req-fraction ${isMatSatisfied ? 'satisfied' : 'deficient'}">${playerQty} / ${mat.required}</span>
            <span class="req-status-icon ${isMatSatisfied ? 'satisfied' : 'deficient'}">${isMatSatisfied ? '✓' : '✗'}</span>
          </div>
        </div>
      `;
    });
  }

  // 檢核不足的警告原因
  let warningHtml = '';
  if (!checkRes.satisfied) {
    let friendlyReason = '';
    if (checkRes.disabledReason === 'recipe_locked') friendlyReason = '配方鎖定：需先完成前置任務。';
    else if (checkRes.disabledReason === 'job_incompatible') friendlyReason = '職業不合：目前職業無法使用此裝備。';
    else if (checkRes.disabledReason === 'gold_deficient') friendlyReason = '金幣不足：冒險者持有金幣無法支付費用。';
    else if (checkRes.disabledReason === 'missing_base_item') friendlyReason = '缺少基底：背包或裝備欄中缺少此強化基底裝備。';
    else if (checkRes.disabledReason === 'materials_deficient') friendlyReason = '素材不足：缺少所需的鍛造/合成素材。';
    
    warningHtml = `<div class="req-warning-box">${friendlyReason}</div>`;
    
    const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
    renderFeedback(npcName, friendlyReason, 'danger');
  } else {
    const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
    renderFeedback(npcName, "鍛造設備已就緒，隨時可以進行交易或強化！", 'success');
  }

  itemRequirementView.innerHTML = `
    <div class="req-item-list">
      ${reqsHtml}
    </div>
    ${warningHtml}
  `;

  // 3. 設定右下按鈕文字與狀態
  const btnText = (currentTab === 'upgrade') ? '⚒ 進行裝備強化' : '💰 購買並放入背包';
  setPrimaryActionText(btnText, !checkRes.satisfied);

  if (checkRes.satisfied) {
    primaryActionBtn.style.cursor = 'pointer';
    primaryActionBtn.removeAttribute('data-disabled-reason');
  } else {
    primaryActionBtn.style.cursor = 'not-allowed';
    primaryActionBtn.setAttribute('data-disabled-reason', checkRes.disabledReason);
  }
}

/**
 * 處理右下主要動作按鈕的執行（含限制狀態的點擊阻擋日誌）
 */
function handlePrimaryAction() {
  if (!currentFixtureData || !selectedItemId) return;

  const item = findItemOrRecipe(selectedItemId);
  if (!item) return;

  if (currentTab === 'owned') {
    if (item.equippedSlot) return;

    const player = currentFixtureData.player;
    const currentJob = player.job;
    const jobCompatible = !item.jobs || item.jobs.includes(currentJob);
    if (!jobCompatible) return;

    if (runtimeClient.isLiveMode()) {
      const actionToDispatch = item.slot === 'weapon' ? 'equip_weapon' : 'equip_equipment';

      logUIAction(actionToDispatch, {
        item_id: selectedItemId
      });

      primaryActionBtn.disabled = true;

      runtimeClient.dispatchAction("workshop_screen", actionToDispatch, { item_id: selectedItemId })
        .then((result) => {
          if (result.screen_model) {
            currentFixtureData = result.screen_model;
            updateCounts();

            // Re-render Header
            playerNameEl.textContent = `冒險者: ${currentFixtureData.player.name}`;
            playerJobEl.textContent = `職業: ${currentFixtureData.player.job} (Lv${currentFixtureData.player.level})`;
            playerGoldEl.textContent = `${currentFixtureData.player.gold}G`;

            switchTab(currentTab, true);
          }

          const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
          if (result.screen_model && result.screen_model.feedback_message) {
            renderFeedback(npcName, `[換裝成功] ` + result.screen_model.feedback_message.text, 'success');
          } else {
            renderFeedback(npcName, `[換裝成功] 成功裝備了 ${item.name}！`, 'success');
          }
        })
        .catch((err) => {
          console.error(err);
          const reason = runtimeClient.errorMessage(err);
          const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
          renderFeedback(npcName, `換裝失敗: ${reason}`, 'danger');
          logUIAction('blocked_action', {
            action: actionToDispatch,
            item_id: selectedItemId,
            disabled_reason: reason
          });
          primaryActionBtn.disabled = false;
        });
    } else {
      const actionToDispatch = item.slot === 'weapon' ? 'equip_weapon' : 'equip_equipment';
      logUIAction(actionToDispatch, {
        item_id: selectedItemId
      });
      const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
      renderFeedback(npcName, `[靜態反饋] 已模擬裝備 ${item.name}。`, 'success');
    }
    return;
  }

  const checkRes = checkRequirements(item);
  
  if (!checkRes.satisfied) {
    // 這裏做為 blocked_action 的 Prototype 除錯日誌
    logUIAction('blocked_action', {
      action: currentTab === 'upgrade' ? 'upgrade_equipment' : 'buy_equipment',
      item_id: selectedItemId,
      disabled_reason: checkRes.disabledReason
    });
    return;
  }

  if (runtimeClient.isLiveMode()) {
    const isUpgrade = currentTab === 'upgrade';
    const actionToDispatch = isUpgrade ? 'upgrade_equipment' : 'buy_equipment';
    const payload = isUpgrade ? { recipe_id: selectedItemId } : { item_id: selectedItemId };

    logUIAction(actionToDispatch, {
      ...payload,
      price: item.price || item.gold
    });

    primaryActionBtn.disabled = true;

    runtimeClient.dispatchAction("workshop_screen", actionToDispatch, payload)
      .then((result) => {
        if (result.screen_model) {
          currentFixtureData = result.screen_model;
          updateCounts();

          // Re-render Header
          playerNameEl.textContent = `冒險者: ${currentFixtureData.player.name}`;
          playerJobEl.textContent = `職業: ${currentFixtureData.player.job} (Lv${currentFixtureData.player.level})`;
          playerGoldEl.textContent = `${currentFixtureData.player.gold}G`;

          switchTab(currentTab, true);
        }

        const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
        if (result.screen_model && result.screen_model.feedback_message) {
          renderFeedback(npcName, `[交易成功] ` + result.screen_model.feedback_message.text, 'success');
        } else {
          renderFeedback(npcName, `[交易成功] 成功處理了 ${item.name}。`, 'success');
        }
      })
      .catch((err) => {
        console.error(err);
        const reason = runtimeClient.errorMessage(err);
        const npcName = (currentTab === 'weapon' || currentTab === 'upgrade') ? '葛雷' : '布琳';
        renderFeedback(npcName, `交易失敗: ${reason}`, 'danger');
        logUIAction('blocked_action', {
          action: actionToDispatch,
          ...payload,
          disabled_reason: reason
        });
        primaryActionBtn.disabled = false;
      });
    return;
  }

  // 交易成功模擬 (只寫 UIAction Log 與文字反饋，不改動 SSOT 數據)
  if (currentTab === 'upgrade') {
    logUIAction('upgrade_equipment', {
      recipe_id: selectedItemId,
      gold: item.gold,
      base_item: item.base_item,
      output: item.output_id
    });
    
    renderFeedback('葛雷', `[強化成功] 葛雷擦亮了冷卻後的護手：「${item.name} 已完成！感受更強大的附魔屬性吧。」`, 'success');
    
  } else {
    logUIAction('buy_equipment', {
      item_id: selectedItemId,
      price: item.price
    });
    
    const npcName = (currentTab === 'weapon') ? '葛雷' : '布琳';
    renderFeedback(npcName, `[交易成功] ${npcName} 將 ${item.name} 妥善包裝好放入你的背包：「金幣收下了，祝你在焦石礦坑好運！」`, 'success');
  }
}

/**
 * 從 Fixture 中檢索裝備或配方
 */
function findItemOrRecipe(id) {
  if (currentTab === 'weapon') {
    return currentFixtureData.weapons.find(w => w.id === id);
  }
  if (currentTab === 'armor') {
    return currentFixtureData.armors.find(a => a.id === id);
  }
  if (currentTab === 'upgrade') {
    return currentFixtureData.upgrades.find(u => u.id === id);
  }
  if (currentTab === 'owned') {
    return getOwnedItemsList().find(o => o.id === id);
  }
  return null;
}

/**
 * 記錄並渲染 UIAction
 */
function logUIAction(actionName, details) {
  const timestamp = new Date().toLocaleTimeString();
  const logObj = { timestamp, action: actionName, ...details };
  
  uiActionLogs.unshift(logObj); // 最新動作在最前
  
  // 限制日誌長度
  if (uiActionLogs.length > 50) {
    uiActionLogs.pop();
  }

  renderDebugLog();
}

/**
 * 渲染除錯視窗內容
 */
function renderDebugLog() {
  debugLogView.innerHTML = '';
  
  uiActionLogs.forEach(log => {
    const row = document.createElement('div');
    row.className = `debug-row ${log.action === 'blocked_action' ? 'blocked-action' : ''}`;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'debug-timestamp';
    timeSpan.textContent = `[${log.timestamp}]`;
    row.appendChild(timeSpan);
    
    // 去除 timestamp 輸出其餘 detail
    const detailsCopy = { ...log };
    delete detailsCopy.timestamp;
    
    const logText = document.createTextNode(JSON.stringify(detailsCopy));
    row.appendChild(logText);
    
    debugLogView.appendChild(row);
  });
}

function renderFeedback(speaker, message, tone = 'gold-bright') {
  const speakerEl = document.getElementById("feedback-speaker");
  if (speakerEl) {
    speakerEl.textContent = speaker;
  }
  // Strip any leading bracketed speaker name like [葛雷]
  let cleanedMessage = message;
  if (speaker && message.startsWith(`[${speaker}]`)) {
    cleanedMessage = message.substring(speaker.length + 2).trim();
  }
  feedbackBar.textContent = cleanedMessage;
  if (tone === 'success') {
    feedbackBar.style.color = 'var(--success-color)';
  } else if (tone === 'danger') {
    feedbackBar.style.color = 'var(--danger-color)';
  } else {
    feedbackBar.style.color = 'var(--gold-bright)';
  }
}

function setPrimaryActionText(text, disabled = false) {
  primaryActionBtn.disabled = disabled;
  const cleanedText = text.replace(/[⚒💰\s]/g, "").trim();
  primaryActionBtn.innerHTML = `
    <svg class="btn-icon-svg" viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.3C.5 6.7.9 9.8 2.9 11.8c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.1z" fill="currentColor"/></svg>
    <span class="btn-text">${cleanedText}</span>
  `;
}
