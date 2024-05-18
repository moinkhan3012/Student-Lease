export default function set_cookie(name, value) {
  document.cookie = name + "=" + value + "; Path=/;";
}
