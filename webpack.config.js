const path = require('path');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const postcssCustomProperties = require('postcss-custom-properties');
const sass = require('sass');

const projectRoot = 'campaignresourcecentre';
const jsSrcDir = `./${projectRoot}/static_src/javascript`;

const options = {
    entry: {
        // multiple entries can be added here
        main: `${jsSrcDir}/main.js`,
        nhsuk: `${jsSrcDir}/nhsuk.js`,
        event: `${jsSrcDir}/event.js`,
        taxonomy: `${jsSrcDir}/wagtail-react-taxonomy.entry.js`
    },
    output: {
        path: path.resolve(`./${projectRoot}/static_compiled/`),
        // based on entry name, e.g. main.js
        filename: 'js/[name].js', // based on entry name, e.g. main.js
    },
    plugins: [
        new CopyPlugin([
            {
                // Copy images to be referenced directly by Django to the "images" subfolder in static files.
                // Ignore CSS background images as these are handled separately below
                from: 'images',
                context: path.resolve(`./${projectRoot}/static_src/`),
                to: path.resolve(`./${projectRoot}/static_compiled/images`),
                ignore: ['cssBackgrounds/*'],
            },
        ]),
        new MiniCssExtractPlugin({
            filename: 'css/[name].css',
        }),
    ],
    module: {
        rules: [
            {
                // tells webpack how to handle js and jsx files
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.(scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            postcssOptions: {
                                plugins: [
                                    autoprefixer(),
                                    postcssCustomProperties(),
                                    cssnano({
                                        preset: 'default',
                                    }),
                                ],
                            }
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            implementation: sass,
                            sassOptions: {
                                outputStyle: 'compressed',
                            },
                        },
                    },
                ],
            },
            {
                // sync font files referenced by the css to the fonts directory
                // the publicPath matches the path from the compiled css to the font file
                // only looks in the fonts folder so pngs in the images folder won't get put in the fonts folder
                test: /\.(woff|woff2)$/,
                include: /fonts/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/',
                        publicPath: '../fonts',
                    },
                },
            },
            {
                // Handles CSS background images in the cssBackgrounds folder
                // Those less than 1024 bytes are automatically encoded in the CSS - see `_test-background-images.scss`
                // the publicPath matches the path from the compiled css to the cssBackgrounds file
                test: /\.(svg|jpg|png)$/,
                include: path.resolve(
                    `./${projectRoot}/static_src/images/cssBackgrounds/`,
                ),
                use: {
                    loader: 'url-loader',
                    options: {
                        fallback: 'file-loader',
                        name: '[name].[ext]',
                        outputPath: 'images/cssBackgrounds/',
                        publicPath: '../images/cssBackgrounds/',
                        limit: 1024,
                    },
                },
            },
        ],
    },
    // externals are loaded via base.html and not included in the webpack bundle.
    externals: {
        // gettext: 'gettext',
    },
};

/*
  If a project requires internationalisation, then include `gettext` in base.html
    via the Django JSi18n helper, and uncomment it from the 'externals' object above.
*/

if (process.env.NODE_ENV === 'development') {
    // Create JS source maps in the dev mode
    // See https://webpack.js.org/configuration/devtool/ for more options
    options.devtool = 'inline-source-map';
}

module.exports = options;
