module.exports = {
  plugins: [
    require('postcss-custom-properties')(),
    require('autoprefixer')(),
    require('cssnano')({ preset: 'default' }),
  ],
};