// 渲染系统列表
export function renderSystemsList() {
    const systemsGrid = document.getElementById('systemsGrid');

    systemsGrid.innerHTML = ''; // 清空现有内容

    // 定义当前可访问的后台系统菜单项
    const availableSystems = [
        {id: 'dashboard', name: '仪表盘', icon: '📊', description: '系统概览', url: 'dashboard.html'},
        {id: 'users', name: '用户管理', icon: '👥', description: '管理平台用户', url: 'users.html'},
        {id: 'products', name: '电商订单管理系统', icon: '📦', description: '管理产品信息', url: 'order_manage/home.html'},
        {id: 'orders', name: '订单管理', icon: '📋', description: '管理订单流程', url: 'orders.html'},
        {id: 'reports', name: '数据报表', icon: '📈', description: '业务数据分析', url: 'reports.html'},
        {id: 'settings', name: '系统设置', icon: '⚙️', description: '系统参数配置', url: 'settings.html'},
        {id: 'logs', name: '操作日志', icon: '📝', description: '用户操作记录', url: 'logs.html'}
    ];

    systemsGrid.style.display = 'grid';
    systemsGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(200px, 1fr))';
    systemsGrid.style.gap = '20px';
    systemsGrid.style.padding='20px';

    availableSystems.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.onclick = () => {
            alert(`即将跳转到 ${item.name} (${item.url})`);
            window.location.href = item.url;
        }; // 演示用，实际应跳转
        card.innerHTML = `
                <div class="system-icon">${item.icon}</div>
                <div class="system-name">${item.name}</div>
                <div class="system-desc">${item.description}</div>
            `;
        systemsGrid.appendChild(card);
    });
}