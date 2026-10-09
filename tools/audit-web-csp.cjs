const fs=require('fs');
const path=require('path');

const files=[];
for(const name of fs.readdirSync('.')){
  if(/\.(?:html|js)$/i.test(name)&&fs.statSync(name).isFile())files.push(name);
}
if(fs.existsSync('assets/js')){
  for(const name of fs.readdirSync('assets/js')){
    if(/\.js$/i.test(name))files.push(path.join('assets/js',name));
  }
}

const issues=[];
const inlineHandler=/<[^>]*\son[a-z]+\s*=\s*["']/gi;
const javascriptUrl=/(?:href|src)\s*=\s*["']\s*javascript:/gi;

for(const file of files){
  const text=fs.readFileSync(file,'utf8');
  for(const match of text.matchAll(inlineHandler))issues.push(`${file}: inline event handler: ${match[0].slice(0,120)}`);
  for(const match of text.matchAll(javascriptUrl))issues.push(`${file}: javascript: URL: ${match[0]}`);

  if(/\.html$/i.test(file)&&/Content-Security-Policy/i.test(text)){
    if(/script-src[^;]*'unsafe-inline'/i.test(text))issues.push(`${file}: script-src must not contain unsafe-inline`);
    const inlineScripts=[...text.matchAll(/<script(?![^>]*\bsrc\s*=)[^>]*>([\s\S]*?)<\/script>/gi)].filter(m=>m[1].trim());
    if(inlineScripts.length)issues.push(`${file}: ${inlineScripts.length} inline <script> block(s) blocked by CSP`);
  }
}

if(issues.length){
  console.error('Web CSP audit failed:');
  for(const issue of issues)console.error(`- ${issue}`);
  process.exit(1);
}
console.log(`Web CSP audit: OK (${files.length} website source files checked; no inline handlers/javascript URLs/blocked inline scripts).`);
