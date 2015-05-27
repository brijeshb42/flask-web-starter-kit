var gulp        = require("gulp"),
    minifyCss   = require("gulp-minify-css"),
    uglify      = require("gulp-uglify"),
    rev         = require("gulp-rev"),
    del         = require("del"),
    plumber     = require("gulp-plumber"),
    usemin      = require("gulp-usemin"),
    htmlmin     = require("gulp-htmlmin"),
    less        = require("gulp-less"),
    livereload  = require('gulp-livereload');

var src = {
    root: "./frontend/",
    html: "./frontend/**//*.html",
    js: "./frontend/static/js/",
    css: "./frontend/static/css/",
    less: "./frontend/static/less/",
    img: "./frontend/static/img/"
};

var dest = {
    root: "./templates/",
    html: "./templates/",
    css: "./templates/static/css/",
    js: "./templates/static/js/",
    img: "./templates/static/img/"
};

gulp.task("clean", function() {
    del([dest.root, src.css], function (err, paths) {
        console.log('Deleted files/folders:\n', paths.join('\n'));
    });
});

gulp.task("copy-img", function() {
    return gulp.src(src.img+"**/*")
        .pipe(gulp.dest(dest.img));
});

gulp.task("js", function() {
    return gulp.src(src.js+"*.js")
        .pipe(gulp.dest(dest.js));
});

gulp.task("js-prod", function() {
    return gulp.src(src.js+"*.js")
        .pipe(uglify())
        .pipe(gulp.dest(dest.js));
});

gulp.task("less", function() {
    return gulp.src(src.less+"style.less")
        .pipe(plumber())
        .pipe(less())
        .pipe(gulp.dest(src.css))
        .pipe(gulp.dest(dest.css))
        .pipe(livereload());
});

gulp.task("less-prod", function() {
    return gulp.src(src.less+"style.less")
        .pipe(plumber())
        .pipe(less())
        .pipe(minifyCss({keepSpecialComments: 0}))
        .pipe(gulp.dest(src.css));
});

gulp.task("usemin", ["less"], function() {
    return gulp.src([src.html])
        .pipe(plumber())
        .pipe(usemin({
            css: [],
            html: [],
            js: []
        }))
        .pipe(gulp.dest(dest.html))
        .pipe(livereload());
});

gulp.task("usemin-prod", ["less-prod", "copy-img"], function() {
    return gulp.src(src.html)
        .pipe(plumber())
        .pipe(usemin({
            css: [rev()],
            html: [htmlmin({
                removeComments: true,
                removeCommentsFromCDATA: true
            })],
            js: [uglify({mangle: false}), rev()]
        }))
        .pipe(gulp.dest(dest.html));
});

gulp.task("htmlmin", ["usemin-prod"], function() {
    return gulp.src(dest.html + "**//*.html")
        .pipe(htmlmin({
            removeComments: true,
            removeCommentsFromCDATA: true
        }))
        .pipe(gulp.dest(dest.html));
});

gulp.task("cssmin", ["htmlmin"], function() {
    return gulp.src(dest.css+"*.css")
        .pipe(minifyCss({keepSpecialComments: 0}))
        .pipe(gulp.dest(dest.css));
});

gulp.task("watch", ["copy-img", "usemin"], function() {
    livereload.listen({
        port: 35729,
        start: true
    });
    console.info('Livereload on PORT '+livereload.options.port);
    gulp.watch(src.html, ["usemin"]);
    gulp.watch(src.less+"*.less", ["less"])
    gulp.watch(src.js+"*.js", ["js"])
});

gulp.task("prod", ["cssmin"]);
gulp.task("default", ["watch"]);
