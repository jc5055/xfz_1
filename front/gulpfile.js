gulp = require('gulp')
cssnano = require('gulp-cssnano')
uglify = require('gulp-uglify')
rename = require('gulp-rename')
imagemin = require('gulp-imagemin')
concat = require('gulp-concat')
bs = require('browser-sync').create()
cache = require('gulp-cache')
sass = require('gulp-sass')
sourcemaps = require('gulp-sourcemaps')
util = require('gulp-util')

var path = {
    'html': './templates/**/*',
    'css': './src/css/**/*',
    'js': './src/js/',
    'images': './src/images/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/',
}

//处理浏览器
gulp.task('bs', function (done) {
    bs.init({
        'server': {
            'basrDir': './'
        }
    })
    done()
})

//处理html
gulp.task('html', function (done) {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())
    done()
})

//处理css task
gulp.task('css', function (done) {
    gulp.src(path.css + '*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(cssnano())
        .pipe(rename({
            "suffix": ".min"
        }))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
    done()
})

//处理js
gulp.task('js', function (done) {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error", util.log))
        .pipe(rename({
            "suffix":".min"
        }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
    done()
})

//处理图片
gulp.task('images', function (done) {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
    done()
})



//监听任务
gulp.task('watch', function (done) {
    gulp.watch(path.html, gulp.series('html'))
    gulp.watch(path.css, gulp.series('css'))
    gulp.watch(path.js, gulp.series('js'))
    gulp.watch(path.images, gulp.series('images'))
    done()
})

//默认任务
// gulp.task('default', gulp.parallel('bs','watch'))
gulp.task('default', gulp.parallel('watch'))
// gulp.task('default', gulp.parallel('watch'))