var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var babel = require('babelify');
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var watchify = require('watchify');


gulp.task( 'styles' , function(){
    gulp
      .src('index.scss')
      .pipe(sass())
      .pipe(rename('app.css'))
      .pipe(gulp.dest('public'));
});

gulp.task( 'assets' , function(){
   gulp
    .src('assets/*')
    .pipe(gulp.dest( 'public' )); 
});

gulp.task('default', ['styles', 'assets']);
