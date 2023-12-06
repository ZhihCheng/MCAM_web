// 當頁面滾動時顯示或隱藏按鈕
window.onscroll = function() {
  scrollFunction();
};

function scrollFunction() {
  var btn = document.getElementById("scrollToTopBtn");

  // 如果滾動高度大於 300，則顯示按鈕，否則隱藏
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    btn.style.display = "block";
  } else {
    btn.style.display = "none";
  }
}
