/**
 * 增强版 fetch 封装 - 支持动态 baseURL
 */
class HttpRequest {
    constructor({baseURL = 'http://localhost:5000', server} = {}) {
        this.baseURL = baseURL;
        this.server = server;
        this.timeout = 10000;
        this.headers = {
            'Content-Type': 'application/json'
        };
        this.requestInterceptor = null;
        this.responseInterceptor = null;
    }

    /**
     * 动态设置 baseURL
     * @param {string} url - 新的 base URL
     */
    setBaseURL(url) {
        this.baseURL = url;
        return this; // 支持链式调用
    }

    /**
     * 动态设置 server
     * @param {string} url - 新的 server
     */
    setServer(url) {
        this.server = url;
        return this; // 支持链式调用
    }

    /**
     * 核心请求方法
     */
    async request(url, options = {}) {
        const {method = 'GET', body = null, noAuth = false, ...customConfig} = options;
        // 拼接请求地址
        const req_url = this.baseURL + this.server;
        // 补充请求的具体方法
        const fullURL = req_url + (url.startsWith('/') ? url : '/' + url);

        const token = localStorage.getItem('Token');
        if (!noAuth && !token) {
            alert('请先登录！');
            window.location.href = '/';
            throw new Error('未登录');
        }

        const headers = {
            ...this.headers,
            ...(token && !noAuth ? {'Authorization': `Bearer ${token}`, 'token': token} : {}),
            ...customConfig.headers
        };

        const config = {
            method: method.toUpperCase(),
            headers,
            ...customConfig,
            body: body ? JSON.stringify(body) : customConfig.body
        };

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        config.signal = controller.signal;

        try {
            const res = await fetch(fullURL, config);

            if (this.responseInterceptor) {
                return await this.responseInterceptor(res);
            }

            if (res.status === 401) {
                alert('登录已失效，请重新登录');
                localStorage.removeItem('Token');
                window.location.href = '/';
                throw new Error('未授权');
            }

            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(`[${res.status}] ${errorText}`);
            }

            return await res.json();

        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('请求超时，请检查网络');
            }
            if (error.name === 'TypeError') {
                console.log(error)
                throw new Error('网络连接失败，请检查服务是否启动');
            }
            throw error;
        } finally {
            clearTimeout(timeoutId);
        }
    }

    // 便捷方法
    get(url, options) {
        return this.request(url, {method: 'GET', ...options});
    }

    post(url, body, options) {
        return this.request(url, {method: 'POST', body, ...options});
    }

    put(url, body, options) {
        return this.request(url, {method: 'PUT', body, ...options});
    }

    delete(url, options) {
        return this.request(url, {method: 'DELETE', ...options});
    }

    // 拦截器
    setRequestInterceptor(fn) {
        this.requestInterceptor = fn;
        return this;
    }

    setResponseInterceptor(fn) {
        this.responseInterceptor = fn;
        return this;
    }
}

// 导出单例
export const request = new HttpRequest({server: ''});
export const UserAuth = new HttpRequest({server: '/UserAuth'});
export const ProdManage = new HttpRequest({server: '/ProdManage'});