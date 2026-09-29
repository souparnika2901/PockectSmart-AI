async function api(url,options={}){const r=await fetch(url,{credentials:"same-origin",...options});let d={};try{d=await r.json()}catch{}if(!r.ok)throw new Error(d.detail||d.message||"Request failed");return d}
document.addEventListener("DOMContentLoaded",()=>{const l=document.getElementById("logoutBtn");if(l)l.onclick=async()=>{await api("/api/logout",{method:"POST"});location.href="/login"};setupAuth("login");setupAuth("register")});
function setupAuth(type){const f=document.getElementById(type+"Form");if(!f)return;f.onsubmit=async e=>{e.preventDefault();const msg=document.getElementById("msg");msg.textContent="";try{const d=await api("/api/"+type,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(f)))});msg.className="success";msg.textContent=d.message;setTimeout(()=>location.href="/dashboard",500)}catch(x){msg.className="error";msg.textContent=x.message}}}
function setupPlanner(type){const f=document.getElementById(type+"Form");if(!f)return;f.onsubmit=async e=>{e.preventDefault();const result=document.getElementById("result");result.innerHTML="<p>Generating...</p>";try{let body;const fd=new FormData(f);if(type==="home")body=JSON.stringify({budget:Number(fd.get("budget")),rooms:fd.get("rooms").split(",").map(x=>x.trim()).filter(Boolean),style:fd.get("style"),notes:fd.get("notes")});else if(type==="party")body=JSON.stringify({budget:Number(fd.get("budget")),guests:Number(fd.get("guests")),event_type:fd.get("event_type"),venue:fd.get("venue"),city:fd.get("city"),notes:fd.get("notes")});else body=fd;const d=await api("/api/generate-"+type,{method:"POST",...(type==="jewelry"?{}:{"headers":{"Content-Type":"application/json"}}),body});renderResult(result,d)}catch(x){result.innerHTML='<p class="error">'+x.message+"</p>"}}}
function renderResult(el, d) {
    let html = '<div class="result">';

    html += '<h2>Recommendations</h2>';
    html += '<p>' + escapeHtml(d.summary) + '</p>';

    html += '<p><span class="tag">Source: ' + escapeHtml(d.source) + '</span></p>';

    html += '<h3>Budget allocation</h3>';

    html += Object.entries(d.allocation)
        .map(([k, v]) =>
            '<p><b>' + escapeHtml(k) + '</b>: ₹' +
            Number(v).toLocaleString("en-IN", {
                maximumFractionDigits: 0
            }) +
            '</p>'
        )
        .join("");

    html += '<h3>Suggestions</h3>';
    html += '<div class="rec-grid">';

    html += d.recommendations
        .map(x =>
            '<div class="rec">' +
            '<span class="tag">' + escapeHtml(x.platform) + '</span>' +
            '<h3>' + escapeHtml(x.name) + '</h3>' +
            '<p class="price">₹' +
            Number(x.estimated_price).toLocaleString("en-IN") +
            '</p>' +
            '<p>' + escapeHtml(x.reason) + '</p>' +
            '<a href="' + x.url +
            '" target="_blank" rel="noopener">Open platform →</a>' +
            '</div>'
        )
        .join("");

    html += '</div>';

    html += '<h3>Tips</h3>';
    html += '<ul>';

    html += d.tips
        .map(x => '<li>' + escapeHtml(x) + '</li>')
        .join("");

    html += '</ul>';

    html += '<p class="muted">' +
        escapeHtml(d.disclaimer) +
        '</p>';

    html += '</div>';

    el.innerHTML = html;
}
async function loadHistory(){const h=document.getElementById("history");if(!h)return;try{const s=await api("/api/session-info");document.getElementById("session").textContent="Signed in as "+s.email;const rows=await api("/api/history");h.innerHTML=rows.length?rows.map(r=>'<article><h3>'+r.planner.toUpperCase()+' — ₹'+Number(r.budget).toLocaleString("en-IN")+'</h3><p>'+escapeHtml(r.result.summary)+'</p><small>'+new Date(r.created_at).toLocaleString()+"</small></article>").join(""):"<article>No recommendations yet.</article>"}catch(x){h.innerHTML='<article class="error">'+x.message+' <a href="/login">Login</a></article>'}}
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
