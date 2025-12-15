/* ========================================
   黑暗模式切换按钮
   ======================================== */

// 主题切换逻辑
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// 读取上次保存的主题或系统偏好
function getPreferredTheme() {
    const saved = localStorage.getItem('theme');
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// 设置主题
function setTheme(theme) {
    if (theme === 'dark') {
        html.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        themeToggle.innerHTML = '🌙 暗色模式';
    } else {
        html.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
        themeToggle.innerHTML = '☀️ 亮色模式';
    }
}

// 初始化
const currentTheme = getPreferredTheme();
setTheme(currentTheme);

// 监听切换
themeToggle.addEventListener('click', () => {
    const isDark = html.classList.contains('dark-mode');
    setTheme(isDark ? 'light' : 'dark');
});

// 可选：监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
    }
});

import { UserAuth } from './api.js';

export async function checkStoredToken() {
    let globalToken = localStorage.getItem('Token')
    let currentUserInfo = JSON.parse(localStorage.getItem('user'))
    if (globalToken && currentUserInfo) {
        try {
            const response = await UserAuth.get('/refresh_token', {
                headers: {
                    'Authorization': `Bearer ${globalToken}`,
                    'token': globalToken,
                    'Content-Type': 'application/json'
                }
            })
            if (response && response.token) {
                localStorage.setItem('Token',response.token)
                // 更新页面上的用户信息显示
                document.getElementById('usernameDisplay').textContent = currentUserInfo.name || '未知用户';
                document.getElementById('userRoleDisplay').textContent = currentUserInfo.role || '未知角色';
                document.getElementById('userAvatar').textContent = (currentUserInfo.name || 'U').charAt(0).toUpperCase();
            } else {
                MsgQ.error(response.msg);
            }
        } catch (e) {
            // MsgQ.error(e);
            console.log('执行 JS 时，DOM 是否加载完成？', document.readyState);
            console.error(e)
        }
    } else {
        // 未登录
        window.location.href = '/login.html';
    }
}

// 登出函数
export function logout() {
    let globalToken = localStorage.getItem('Token')
    let currentUserInfo = JSON.parse(localStorage.getItem('user'))
    // 如果有全局token，调用登出API
    if (globalToken && currentUserInfo) {
        const response = UserAuth.post('/logout', {
            name: currentUserInfo.name,
            uid: currentUserInfo.uid
        }, {
            headers: {
                'Authorization': `Bearer ${globalToken}`,
                'token': globalToken,
                'Content-Type': 'application/json'
            },
            baseUrl: '/UserAuth'
        })
    }

    // 清空用户信息显示
    document.getElementById('usernameDisplay').textContent = '未登录';
    document.getElementById('userRoleDisplay').textContent = '-';
    document.getElementById('userAvatar').textContent = 'U';

    // 清除localStorage中的token
    localStorage.removeItem('Token');
    localStorage.removeItem('user');

    window.location.href = '/login.html';
}


/* ========================================
   加载动画
   ======================================== */

export class Loading {
    static instances = new Map(); // 存储每个 target 的加载实例

    /**
     * 显示加载动画
     * @param {Object} options
     * @param {string} options.target - 目标元素的 id
     * @param {string} options.text - 显示的文字
     * @param {string} options.type - 'spinner' | 'progress'
     * @param {number} options.progress - 进度百分比 (0-100)
     */
    static show(options = {}) {
        const {
            target,
            text = '加载中...',
            type = 'spinner',
            progress = 0
        } = options;

        const $target = document.getElementById(target);
        if (!$target) {
            console.warn(`Loading: 未找到 id="${target}" 的元素`);
            return;
        }

        // 如果已存在，先移除
        this.hide(target);

        // 设置目标容器为相对定位
        if ($target.style.position === '') {
            $target.style.position = 'relative';
        }
        $target.classList.add('loading-container');

        // 创建加载层
        const $overlay = document.createElement('div');
        $overlay.className = 'loading-overlay';
        $overlay.id = `loading-${target}`;

        // 创建内容
        const $content = document.createElement('div');
        $content.innerHTML = `<p class="loading-text">${text}</p>`;

        // 根据类型添加动画
        if (type === 'progress') {
            $content.innerHTML = `
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${progress}%"></div>
        </div>
        <p class="loading-text">${text}</p>
      `;
        } else {
            // 默认 spinner
            $content.innerHTML = `
        <div class="spinner"></div>
        <p class="loading-text">${text}</p>
      `;
        }

        $overlay.appendChild($content);
        $target.appendChild($overlay);

        // 保存实例
        this.instances.set(target, {overlay: $overlay, type, $target});
    }

    /**
     * 更新加载状态（用于进度条）
     * @param {string} target
     * @param {Object} updates - { text, progress }
     */
    static update(target, updates) {
        const instance = this.instances.get(target);
        if (!instance) return;

        const {type, overlay} = instance;

        if (updates.text) {
            const $text = overlay.querySelector('.loading-text');
            if ($text) $text.textContent = updates.text;
        }

        if (updates.progress !== undefined && type === 'progress') {
            const $fill = overlay.querySelector('.progress-fill');
            if ($fill) $fill.style.width = `${Math.min(100, Math.max(0, updates.progress))}%`;
        }
    }

    /**
     * 隐藏加载动画
     * @param {string} target - 目标元素 id
     */
    static hide(target) {
        const instance = this.instances.get(target);
        if (instance) {
            instance.overlay.remove();
            this.instances.delete(target);
        }
    }
}

// 暴露为全局变量（或用模块化导入）
// window.Loading = Loading;

// MsgQ - 静态消息队列工具类

export class MsgQ {
    static MAX_VISIBLE = 3;                    // 最多同时显示 3 条
    static queue = [];                         // 待显示队列
    static visible = [];                       // 当前显示的消息元素
    static container = null;
    static duration = 3000;                    // 消息显示时间 ms
    static action_time = 300;                  // 动画时间 ms

    // 初始化容器
    static initContainer() {
        this.container = document.getElementById('msgq-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'msgq-container';
            this.container.className = 'alert-div'
            document.body.appendChild(this.container);
        }
    }

    // 创建单条消息元素
    static createItem(message, type) {
        const item = document.createElement('div');
        item.className = `alert alert-${type}`;
        item.innerHTML = `
      <span>${message}</span>
      <span class="close-btn" onclick="MsgQ.close(this)">×</span>
    `;
        return item;
    }

    // 显示一条消息
    static showOne(message, type = 'info', duration = this.duration) {
        const item = this.createItem(message, type);
        this.container.appendChild(item);

        // 强制重排，触发动画
        void item.offsetWidth;
        item.classList.add('show');

        // 添加到 visible 数组
        this.visible.push(item);

        // 设置自动关闭
        let timer;
        if (duration !== Infinity) {
            timer = setTimeout(() => {
                this.hideOne(item);
            }, duration);
        }

        // 悬停暂停
        item.onmouseenter = () => {
            if (timer) clearTimeout(timer);
        };
        item.onmouseleave = () => {
            if (duration !== Infinity) {
                timer = setTimeout(() => this.hideOne(item), duration);
            }
        };

        // 返回 Promise，可用于链式调用（可选）
        return item;
    }

    // 隐藏并移除一条消息
    static hideOne(item) {
        item.classList.remove('show');
        setTimeout(() => {
            if (item.parentNode) {
                item.parentNode.removeChild(item);
            }
            // 从 visible 中移除
            const index = this.visible.indexOf(item);
            if (index > -1) {
                this.visible.splice(index, 1);
            }
            // 补充下一条
            this.fillNext();
        }, this.action_time);
    }

    // 从队列中取出下一条并显示
    static fillNext() {
        if (this.visible.length >= this.MAX_VISIBLE) return;
        if (this.queue.length === 0) return;

        const {message, type, duration} = this.queue.shift();
        this.showOne(message, type, duration);
    }

    // 添加新消息（入队）
    static push(message, type = 'info', duration = this.duration) {
        this.initContainer();

        // 如果当前显示不足 5 条，直接显示
        if (this.visible.length < this.MAX_VISIBLE) {
            this.showOne(message, type, duration);
        } else {
            // 否则加入待显示队列
            this.queue.push({message, type, duration});
        }
    }

    // 手动关闭某条消息（通过 close 按钮调用）
    static close(closeBtn) {
        const item = closeBtn.closest('.alert');
        if (item) {
            this.hideOne(item);
        }
    }

    // 清空所有（可选）
    static clearAll() {
        this.queue = [];
        Array.from(this.visible).forEach(item => this.hideOne(item));
    }

    // 快捷方法
    static success(message, duration = this.duration) {
        this.push(message, 'success', duration);
    }

    static error(message, duration = this.duration) {
        this.push(message, 'error', duration);
    }

    static warning(message, duration = this.duration) {
        this.push(message, 'warning', duration);
    }

    static info(message, duration = this.duration) {
        this.push(message, 'info', duration);
    }
}