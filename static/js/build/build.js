/*
 * Build.js for require.js optimizer (r.js).
 */

({
    baseUrl: '.',
    mainConfigFile: './main.js',
    name: 'main',
    out: '../main.min.js',
    paths: {
        requireLib: '../vendor/requirejs/require',
        underscore: 'empty:',
        restangular: 'empty:'
    },
    include: ['requireLib']
})
