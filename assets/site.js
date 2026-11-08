(() => {
  'use strict';
  const filterBar = document.querySelector('.filter-bar');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const projects = [...document.querySelectorAll('[data-category]')];
  const status = document.querySelector('#filter-status');
  if (filterBar && filters.length && projects.length) {
    filterBar.hidden = false;
    filters.forEach(button => button.addEventListener('click', () => {
      filters.forEach(item => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      projects.forEach(project => {
        project.hidden = button.dataset.filter !== 'all' && project.dataset.category !== button.dataset.filter;
      });
      const count = projects.filter(project => !project.hidden).length;
      status.textContent = `显示 ${count} 个${button.dataset.filter === 'all' ? '' : button.dataset.filter === 'rhythm' ? '音游' : '硬件'}项目`;
    }));
  }
  const channelControls = document.querySelector('.audio-controls');
  const channels = [...document.querySelectorAll('[data-channel]')];
  if (channelControls && channels.length) {
    channelControls.hidden = false;
    channels.forEach(button => button.addEventListener('click', () => {
      const index = Number(button.dataset.channel) - 1;
      channels.forEach(item => {
        const selected = item === button;
        item.classList.toggle('selected', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
      document.querySelectorAll('.audio-inputs span').forEach((item, i) => item.classList.toggle('selected', i === index));
      document.querySelectorAll('.audio-wires i').forEach((item, i) => item.classList.toggle('selected', i === index));
      const diagram = document.querySelector('.audio-diagram');
      diagram.setAttribute('aria-label', `原理示意：输入通道 ${index + 1} 经 Pico 控制继电器切换至输出，不连接硬件`);
    }));
  }
  const year = document.querySelector('#year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
