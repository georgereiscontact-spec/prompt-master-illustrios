(() => {
  const keys=['promptMasterV2','promptMasterMyPrompts','promptMasterPrompts','promptMasterLoras'];
  const snapshot=()=>Object.fromEntries(keys.map(k=>[k,localStorage.getItem(k)]));
  const apply=data=>Object.entries(data||{}).forEach(([k,v])=>v===null?localStorage.removeItem(k):localStorage.setItem(k,v));
  async function load(){try{const r=await fetch('/api/data');if(r.ok){const d=await r.json();if(Object.keys(d).length){apply(d);location.reload()}}}catch(e){}}
  async function save(){try{await fetch('/api/data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(snapshot())})}catch(e){}}
  load(); setInterval(save,1500); window.addEventListener('beforeunload',save);
})();
