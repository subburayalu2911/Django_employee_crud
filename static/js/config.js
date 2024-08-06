
function get_domain(){
  let SITE_URL = "";
  const windowLocation = window.location;
  if (windowLocation.protocol) {
    SITE_URL += windowLocation.protocol + "//";
  }
  if (windowLocation.hostname) {
    SITE_URL += windowLocation.hostname;
  
  }
  if (windowLocation.port) {
    SITE_URL += ":" + windowLocation.port;  
  }
  return SITE_URL;
}
