const host = process.env.PROXY_HOST || 'localhost';
const port = process.env.PROXY_PORT || '8000';

module.exports = {
    proxy: {
        target: `${host}:${port}`,
        proxyOptions: {
            changeOrigin: false,
        },
    },
    serveStatic: [
        {
            route: '/static',
            dir: 'campaignresourcecentre/static_compiled',
        },
    ],
    files: 'campaignresourcecentre/static_compiled',
};
