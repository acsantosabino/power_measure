var path = require('path')

module.exports = {
    entry: {
        measure: path.resolve(__dirname, "measure.jsx"),
    },
    output: {
        path: path.resolve(__dirname, "templates/js"),
        filename: "measure.js"
    },
    module: {
        loaders: [
            {
              test: /\.jsx$/,
              exclude: /(node_modules|bower_componentes)/,
              loader: "babel",
              query: {
                "presets": ["react", "es2015"]
              }
            }
        ]
    },
    resolve: {
      extensions: ["", ".js", ".jsx"]
    },
};
