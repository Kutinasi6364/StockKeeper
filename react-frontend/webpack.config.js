const path = require('path');

module.exports = {
    mode: 'development',
    entry: './src/index.tsx', //buildするファイル
    output: {
        filename: 'bundle.js', //build後のファイル名
        path: path.join(__dirname, './build/static/js') //buildファイルが作成される場所
    },
    module: {
        rules: [
			//JavaScriptの場合のloader設定
			{
				test: /\.js[x]?$/,  
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: [
							'@babel/preset-env',
							'@babel/preset-react' 
						],
						plugins: ['@babel/plugin-syntax-jsx'] 
					}
				}
			},
        
			//Typescriptの場合のloader設定
			{
				test: /\.ts[x]?$/,  
				exclude: /node_modules/,
				use: 'ts-loader',
			},

			//CSSファイルを読み込むための設定
			{
				test: /\.css$/,
				use: [
					'style-loader',
					'css-loader',
					// {
					// 	loader: 'postcss-loader',
					// 	options: {
					// 		postcssOptions: {
					// 			ident: 'postcss',
					// 			plugins: [
					// 				require('tailwindcss'),
					// 				require('autoprefixer'),
					// 			],
					// 		},
					// 	},
					// },
				],
			},
		],	
    },

    resolve: {
        extensions: ['.js', '.jsx', '.json', '.ts', '.tsx']
	}
};
