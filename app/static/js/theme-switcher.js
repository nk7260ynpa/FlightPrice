/**
 * FlightPrice 主題切換器
 *
 * 負責：
 *   1. 綁定 navbar dropdown 中所有 [data-theme-value] 選項的 click 事件
 *   2. 將使用者選擇套用至 <html data-theme>
 *   3. 以 localStorage key `flightprice-theme` 持久化
 *   4. 派發 CustomEvent('themechange')，供 Chart.js 等模組監聽重繪
 *   5. 初始化時根據 localStorage 標記當前選項 aria-current
 *
 * 本腳本不得呼叫頁面重新載入 API；主題切換全程不刷新頁面。
 */
(function () {
  'use strict';

  /** 合法主題白名單。 */
  var VALID_THEMES = ['scoot', 'eva', 'china-airlines', 'starlux'];

  /** localStorage 儲存主題值的 key。 */
  var STORAGE_KEY = 'flightprice-theme';

  /**
   * 從 localStorage 讀取已儲存的主題，若無或不合法則回傳預設 'scoot'。
   * @returns {string} 合法主題值。
   */
  function readStoredTheme() {
    try {
      var t = localStorage.getItem(STORAGE_KEY);
      if (VALID_THEMES.indexOf(t) >= 0) {
        return t;
      }
    } catch (e) {
      // localStorage 不可用（例如私密模式）：退回預設。
    }
    return 'scoot';
  }

  /**
   * 套用主題並同步所有副作用。
   * @param {string} value 合法主題值。
   */
  function applyTheme(value) {
    if (VALID_THEMES.indexOf(value) < 0) {
      return;
    }

    // 1. 設定 <html data-theme>
    document.documentElement.setAttribute('data-theme', value);

    // 2. 持久化到 localStorage
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {
      // 忽略儲存失敗；記憶體內主題仍可切換
    }

    // 3. 更新 dropdown 內選項 aria-current 標示
    updateMenuAriaCurrent(value);

    // 4. 派發 themechange CustomEvent 供其他模組監聽
    var event = new CustomEvent('themechange', {
      detail: { theme: value },
    });
    document.dispatchEvent(event);
  }

  /**
   * 更新 dropdown 中各選項的 aria-current 屬性。
   * @param {string} activeValue 當前啟用的主題值。
   */
  function updateMenuAriaCurrent(activeValue) {
    var items = document.querySelectorAll('[data-theme-value]');
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      if (item.getAttribute('data-theme-value') === activeValue) {
        item.setAttribute('aria-current', 'true');
      } else {
        item.removeAttribute('aria-current');
      }
    }
  }

  /**
   * 綁定 dropdown 中所有 [data-theme-value] 按鈕的 click 事件。
   */
  function bindMenuItems() {
    var items = document.querySelectorAll('[data-theme-value]');
    for (var i = 0; i < items.length; i++) {
      items[i].addEventListener('click', function (ev) {
        ev.preventDefault();
        var target = ev.currentTarget || ev.target;
        var value = target.getAttribute('data-theme-value');
        applyTheme(value);
      });
    }
  }

  /**
   * 頁面載入時的初始化：以 localStorage 當前值標示 aria-current。
   * data-theme 屬性已由 base.html <head> inline FOUC script 設定，此處
   * 不必重新設定 document.documentElement，以避免覆寫使用者最新選擇。
   */
  function init() {
    var current = readStoredTheme();
    updateMenuAriaCurrent(current);
    bindMenuItems();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
