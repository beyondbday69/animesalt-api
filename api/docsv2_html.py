DOCSV2_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMART DOCS V2</title>
    <style>
        :root {
            --bg: #000000;
            --fg: #ffffff;
            --border: 2px solid #ffffff;
            --font: 'Courier New', Courier, monospace;
        }
        
        * { 
            box-sizing: border-box; 
            outline: none !important; 
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: var(--font);
            background-color: var(--bg);
            color: var(--fg);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 1200px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: var(--border);
            padding-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        /* Search only */
        .search-container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto 25px;
            position: relative;
            z-index: 1000;
        }
        .search-bar {
            display: flex;
            gap: 0;
            border: var(--border);
        }
        .search-bar input {
            flex: 1;
            padding: 15px;
            border: none;
            background: var(--bg);
            color: var(--fg);
            font-size: 16px;
            font-family: var(--font);
            border-right: var(--border);
        }
        .search-bar button {
            padding: 0 25px;
            border: none;
            background: var(--fg);
            color: var(--bg);
            cursor: pointer;
            font-weight: bold;
            font-family: var(--font);
            text-transform: uppercase;
        }
        .search-bar button:hover { background: #cccccc; }

        .search-results {
            position: absolute;
            top: 100%; left: 0; right: 0;
            background: var(--bg);
            border: var(--border);
            border-top: none;
            max-height: 400px;
            overflow-y: auto;
            z-index: 1001;
            display: none;
        }
        .search-results.show { display: block; }
        .search-item {
            padding: 12px;
            display: flex;
            gap: 15px;
            cursor: pointer;
            border-bottom: var(--border);
            align-items: center;
            text-transform: uppercase;
        }
        .search-item:last-child { border-bottom: none; }
        .search-item:hover { background: var(--fg); color: var(--bg); }
        .search-item img { width: 45px; height: 60px; object-fit: cover; border: var(--border); filter: grayscale(100%); }

        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            justify-content: center;
            align-items: center;
        }
        .btn-home {
            background: var(--bg);
            color: var(--fg);
            padding: 10px 20px;
            border: var(--border);
            font-weight: bold;
            cursor: pointer;
            font-family: var(--font);
            text-transform: uppercase;
            box-shadow: 4px 4px 0 var(--fg);
            transition: all 0.1s;
        }
        .btn-home:active { transform: translate(4px, 4px); box-shadow: none; }

        .toggle-container {
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--bg);
            padding: 8px 16px;
            border: var(--border);
            font-size: 13px;
            text-transform: uppercase;
            font-weight: bold;
        }
        .switch { position: relative; width: 40px; height: 20px; border: var(--border); background: var(--bg); }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: transparent; transition: .2s;
        }
        .slider:before {
            position: absolute; content: ""; height: 12px; width: 12px; left: 2px; bottom: 2px;
            background-color: var(--fg); transition: .2s;
        }
        input:checked + .slider { background-color: var(--fg); }
        input:checked + .slider:before { transform: translateX(20px); background-color: var(--bg); }

        /* Layout Grid */
        .layout {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 25px;
        }
        @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } }

        .panel {
            background: var(--bg);
            border: var(--border);
            padding: 20px;
            box-shadow: 8px 8px 0 var(--fg);
        }
        
        .anime-info img {
            width: 100%;
            border: var(--border);
            filter: grayscale(100%);
            transition: filter 0.3s;
        }
        .anime-info img:hover { filter: grayscale(0%); }
        .watchlist-btn {
            background: var(--bg); color: var(--fg); padding: 10px; border: var(--border);
            cursor: pointer; font-size: 13px; margin-top: 15px; width: 100%;
            text-transform: uppercase; font-weight: bold; font-family: var(--font);
            box-shadow: 4px 4px 0 var(--fg);
            transition: all 0.1s;
        }
        .watchlist-btn:active { transform: translate(4px, 4px); box-shadow: none; }
        .watchlist-btn.active { background: var(--fg); color: var(--bg); box-shadow: none; transform: translate(4px, 4px); }

        .seasons { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; }
        .btn-s {
            background: var(--bg); color: var(--fg); border: var(--border); padding: 8px 14px;
            cursor: pointer; font-size: 13px; font-weight: bold; font-family: var(--font); text-transform: uppercase;
        }
        .btn-s.active { background: var(--fg); color: var(--bg); }
        .btn-s:hover:not(.active) { background: #333; }

        .episodes {
            max-height: 500px;
            overflow-y: scroll;
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 15px;
            border-top: var(--border);
            padding-top: 15px;
        }
        .ep-card {
            background: var(--bg); padding: 10px; display: flex; align-items: center;
            gap: 15px; cursor: pointer; border: var(--border); text-transform: uppercase;
        }
        .ep-card:hover { background: var(--fg); color: var(--bg); }
        .ep-card.active { background: var(--fg); color: var(--bg); }
        .ep-card img { width: 90px; height: 50px; object-fit: cover; border: var(--border); filter: grayscale(100%); }

        /* Player */
        .player-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: var(--border); padding-bottom: 10px; }
        .player-container {
            width: 100%; aspect-ratio: 16/9; background: var(--bg); border: var(--border);
            box-shadow: 8px 8px 0 var(--fg); margin-bottom: 25px;
        }
        iframe { width: 100%; height: 100%; border: none; filter: grayscale(100%); transition: filter 0.3s; }
        iframe:hover { filter: grayscale(0%); }

        .server-list { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
        .btn-pill {
            background: var(--bg); color: var(--fg); padding: 10px 18px; border: var(--border);
            cursor: pointer; font-size: 13px; font-weight: bold; font-family: var(--font); text-transform: uppercase;
            box-shadow: 3px 3px 0 var(--fg);
            transition: all 0.1s;
        }
        .btn-pill:active { transform: translate(3px, 3px); box-shadow: none; }
        .btn-pill.active { background: var(--fg); color: var(--bg); box-shadow: none; transform: translate(3px,3px); }

        /* Home Sections */
        .home-section { margin-bottom: 40px; border-top: var(--border); padding-top: 20px; }
        .home-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 20px; }
        .anime-card {
            background: var(--bg); border: var(--border); cursor: pointer;
            position: relative; box-shadow: 6px 6px 0 var(--fg);
            transition: all 0.1s;
        }
        .anime-card:active { transform: translate(4px, 4px); box-shadow: 2px 2px 0 var(--fg); }
        .anime-card img { width: 100%; height: 240px; object-fit: cover; filter: grayscale(100%); border-bottom: var(--border); transition: filter 0.3s;}
        .anime-card:hover img { filter: grayscale(0%); }
        .card-info { padding: 12px; }
        .card-title { font-size: 14px; font-weight: bold; text-transform: uppercase; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        
        .history-badge { font-size: 11px; font-weight: bold; margin-top: 4px; border-top: 1px dashed var(--fg); padding-top: 4px; }
        .remove-icon {
            position: absolute; top: 8px; right: 8px; background: var(--bg); color: var(--fg);
            width: 24px; height: 24px; border: var(--border); display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: bold; opacity: 0; z-index: 10;
        }
        .anime-card:hover .remove-icon { opacity: 1; }
        .remove-icon:hover { background: var(--fg); color: var(--bg); }

        .loader {
            border: 4px solid var(--bg); border-top-color: var(--fg); border-left-color: var(--fg);
            width: 40px; height: 40px; animation: spin 0.5s steps(4) infinite; margin: 20px auto;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .hidden { display: none !important; }
        ::-webkit-scrollbar { width: 12px; border-left: var(--border); }
        ::-webkit-scrollbar-thumb { background: var(--fg); }
        ::-webkit-scrollbar-track { background: var(--bg); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 onclick="fetchHome()" style="cursor:pointer; font-size:40px; font-weight:900; margin:0;">[ SMART_DOCS_V2 ]</h1>
        </header>

        <div class="search-container">
            <div class="search-bar">
                <input type="text" id="searchQuery" placeholder="SEARCH ANIME..." autocomplete="off">
                <button onclick="doSearch()">[ SEARCH ]</button>
            </div>
            <div id="searchResults" class="search-results"></div>
        </div>

        <div class="controls">
            <button class="btn-home" onclick="fetchHome()">[ HOME ]</button>
            <div class="toggle-container">
                <span>ADS_BLOCK</span>
                <label class="switch">
                    <input type="checkbox" id="blockRedirects" onchange="updatePlayerSandbox()">
                    <span class="slider"></span>
                </label>
            </div>
        </div>

        <div id="mainLoader" class="loader hidden"></div>

        <div id="homeLayout">
            <div id="personalSections"></div>
            <div id="apiHomeSections"></div>
        </div>

        <div class="layout hidden" id="contentLayout">
            <div class="sidebar">
                <div class="panel anime-info">
                    <img id="animePoster" src="">
                    <h2 id="animeTitle" style="margin:15px 0 5px; font-size:22px; text-transform:uppercase;"></h2>
                    <button id="watchlistBtn" class="watchlist-btn" onclick="toggleWatchlist()">[+] WATCHLIST</button>
                    <p id="animeGenres" style="font-size:13px; font-weight:bold; margin-top:10px; border-bottom:var(--border); padding-bottom:10px;"></p>
                    <p id="animeDesc" style="font-size:14px; line-height:1.4; margin-top:15px;"></p>
                    <div id="animeExtra" style="margin-top:15px; font-size:12px; display:grid; grid-template-columns:1fr 1fr; gap:10px; border-top:var(--border); padding-top:15px;"></div>
                    
                    <h3 style="margin-top:25px; font-size:16px; border-bottom:var(--border); padding-bottom:5px;">[ SEASONS ]</h3>
                    <div class="seasons" id="seasonsList"></div>
                </div>
                
                <div class="panel" style="margin-top:20px;">
                    <h3 style="margin:0; font-size:16px; border-bottom:var(--border); padding-bottom:5px;">[ EPISODES ]</h3>
                    <div id="epLoader" class="loader hidden"></div>
                    <div class="episodes" id="episodesList"></div>
                </div>
            </div>

            <div class="main">
                <div class="panel" id="playerPanel">
                    <div class="player-header">
                        <h2 id="nowPlaying" style="font-size:18px; margin:0; text-transform:uppercase;"></h2>
                        <div style="display:flex; gap:8px;">
                            <button class="btn-home" id="btnPrev" onclick="playPrev()" style="padding:6px 12px;">PREV</button>
                            <button class="btn-home" id="btnNext" onclick="playNext()" style="padding:6px 12px;">NEXT</button>
                        </div>
                    </div>
                    <div id="nextEpTime" style="font-weight:bold; font-size:12px; margin-bottom:10px; border:1px solid #fff; display:inline-block; padding:5px;"></div>
                    <div id="vmolyWarning" class="hidden" style="font-weight:bold; font-size:12px; margin-bottom:10px; background:#fff; color:#000; padding:5px;">[!] VMOLY UNAVAILABLE. ADS MAY PLAY.</div>
                    
                    <div class="player-container">
                        <iframe id="videoPlayer" allowfullscreen></iframe>
                    </div>

                    <div class="server-list" id="serversList"></div>
                    <div class="server-list" id="downloadsList"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let history = JSON.parse(localStorage.getItem('s_history')) || [];
        let watchlist = JSON.parse(localStorage.getItem('s_watchlist')) || [];
        let favServer = localStorage.getItem('s_server') || '';
        let currentAnime = null;
        let epList = [];
        let epIdx = -1;

        const sInp = document.getElementById('searchQuery');
        let sT;
        sInp.addEventListener('input', (e) => {
            clearTimeout(sT);
            if(e.target.value.length > 2) sT = setTimeout(doSearch, 400);
            else document.getElementById('searchResults').classList.remove('show');
        });

        async function doSearch() {
            const q = sInp.value.trim();
            const resBox = document.getElementById('searchResults');
            resBox.innerHTML = '<div class="loader"></div>';
            resBox.classList.add('show');
            try {
                const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(q)}`);
                const json = await res.json();
                resBox.innerHTML = '';
                if(json.success && json.results) {
                    json.results.slice(0,12).forEach(a => {
                        const d = document.createElement('div');
                        d.className = 'search-item';
                        d.innerHTML = `<img src="${a.image}"> <div><b>${a.title}</b><br><small>${a.slug}</small></div>`;
                        d.onclick = () => { resBox.classList.remove('show'); sInp.value=''; loadAnime(a.slug); };
                        resBox.appendChild(d);
                    });
                }
            } catch(e){}
        }

        async function fetchHome() {
            window.scrollTo({top:0, behavior:'smooth'});
            document.getElementById('contentLayout').classList.add('hidden');
            document.getElementById('homeLayout').classList.remove('hidden');
            document.getElementById('mainLoader').classList.remove('hidden');
            renderPersonal();
            try {
                const res = await fetch(`${API_BASE}/api/home`);
                const json = await res.json();
                const container = document.getElementById('apiHomeSections');
                container.innerHTML = '';
                if(json.success && json.data) {
                    for(const [k, arr] of Object.entries(json.data)) {
                        if(!arr.length) continue;
                        let h = `<div class="home-section"><h2>[ ${k.replace(/_/g,' ').toUpperCase()} ]</h2><div class="home-grid">`;
                        arr.forEach(a => {
                            h += `<div class="anime-card" onclick="loadAnime('${a.slug}')"><img src="${a.image}" loading="lazy"><div class="card-info"><div class="card-title">${a.title}</div></div></div>`;
                        });
                        container.innerHTML += h + '</div></div>';
                    }
                }
            } catch(e){}
            document.getElementById('mainLoader').classList.add('hidden');
        }

        function renderPersonal() {
            const container = document.getElementById('personalSections');
            container.innerHTML = '';
            if(history.length) {
                let h = `<div class="home-section"><h2>[ CONTINUE WATCHING ]</h2><div class="home-grid">`;
                history.forEach(i => {
                    h += `<div class="anime-card" onclick="loadAnime('${i.slug}', '${i.eid}')"><div class="remove-icon" onclick="event.stopPropagation(); history=history.filter(x=>x.slug!=='${i.slug}'); localStorage.setItem('s_history', JSON.stringify(history)); renderPersonal();">X</div><img src="${i.image}"><div class="card-info"><div class="card-title">${i.title}</div><div class="history-badge">${i.et}</div></div></div>`;
                });
                container.innerHTML += h + '</div></div>';
            }
            if(watchlist.length) {
                let h = `<div class="home-section"><h2>[ MY WATCHLIST ]</h2><div class="home-grid">`;
                watchlist.forEach(i => {
                    h += `<div class="anime-card" onclick="loadAnime('${i.slug}')"><div class="remove-icon" onclick="event.stopPropagation(); watchlist=watchlist.filter(x=>x.slug!=='${i.slug}'); localStorage.setItem('s_watchlist', JSON.stringify(watchlist)); renderPersonal();">X</div><img src="${i.image}"><div class="card-info"><div class="card-title">${i.title}</div></div></div>`;
                });
                container.innerHTML += h + '</div></div>';
            }
        }

        async function loadAnime(slug, autoEid = null) {
            window.scrollTo({top:0, behavior:'smooth'});
            document.getElementById('homeLayout').classList.add('hidden');
            document.getElementById('mainLoader').classList.remove('hidden');
            const wa = document.getElementById('watchArea'); if(wa) wa.classList.add('hidden');
            document.getElementById('videoPlayer').src = '';

            try {
                const res = await fetch(`${API_BASE}/api/anime/${slug}`);
                const json = await res.json();
                if(json.success && json.data) {
                    const d = json.data;
                    currentAnime = { slug, title: d.title, image: d.thumbnail };
                    document.getElementById('animeTitle').innerText = d.title;
                    document.getElementById('animePoster').src = d.thumbnail;
                    document.getElementById('animeDesc').innerText = d.description;
                    document.getElementById('animeGenres').innerText = (d.genres||[]).join(' | ');
                    
                    const extra = document.getElementById('animeExtra');
                    extra.innerHTML = '';
                    if(d.information) {
                        for(const [k,v] of Object.entries(d.information)) {
                            if(!v || v==='N/A') continue;
                            extra.innerHTML += `<div><b>${k.replace(/_/g,' ').toUpperCase()}</b><div>${v}</div></div>`;
                        }
                    }

                    const sDiv = document.getElementById('seasonsList'); sDiv.innerHTML = '';
                    if(d.seasons) {
                        d.seasons.forEach((s, i) => {
                            const b = document.createElement('button');
                            b.className = `btn-s ${i===0?'active':''}`;
                            b.innerText = s.name;
                            b.onclick = () => { document.querySelectorAll('.btn-s').forEach(x=>x.classList.remove('active')); b.classList.add('active'); fetchEps(s.id, autoEid); };
                            sDiv.appendChild(b);
                        });
                        fetchEps(d.seasons[0].id, autoEid);
                    }
                    updateWatchBtn();
                    document.getElementById('contentLayout').classList.remove('hidden');
                }
            } catch(e){}
            document.getElementById('mainLoader').classList.add('hidden');
        }

        async function fetchEps(sid, autoEid) {
            document.getElementById('epLoader').classList.remove('hidden');
            const grid = document.getElementById('episodesList'); grid.innerHTML = '';
            try {
                const res = await fetch(`${API_BASE}/api/episodes/${sid}`);
                const json = await res.json();
                if(json.success && json.data.episodes) {
                    epList = json.data.episodes;
                    epList.forEach((ep, i) => {
                        const div = document.createElement('div');
                        div.className = 'ep-card'; div.id = `ep-${ep.id}`;
                        div.innerHTML = `<img src="${ep.thumbnail}"> <div><b>${ep.title}</b></div>`;
                        div.onclick = () => fetchStream(ep.id, ep.title, i);
                        grid.appendChild(div);
                        if(autoEid === ep.id) fetchStream(ep.id, ep.title, i);
                    });
                }
            } catch(e){}
            document.getElementById('epLoader').classList.add('hidden');
        }

        async function fetchStream(eid, title, idx) {
            epIdx = idx;
            const wa = document.getElementById('watchArea'); if(wa) wa.classList.remove('hidden');
            document.getElementById('nowPlaying').innerText = title;
            document.querySelectorAll('.ep-card').forEach(x=>x.classList.remove('active'));
            document.getElementById(`ep-${eid}`)?.classList.add('active');
            
            document.getElementById('btnPrev').disabled = idx <= 0;
            document.getElementById('btnNext').disabled = idx >= epList.length - 1;
            
            const player = document.getElementById('videoPlayer');
            
            history = history.filter(x=>x.slug !== currentAnime.slug);
            history.unshift({...currentAnime, eid, epTitle: title});
            localStorage.setItem('s_history', JSON.stringify(history.slice(0, 20)));

            try {
                const res = await fetch(`${API_BASE}/api/stream/${eid}`);
                const json = await res.json();
                if(json.success && json.data) {
                    const d = json.data;
                    document.getElementById('nextEpTime').innerText = d.next_episode_time ? `NEXT EPISODE: ${d.next_episode_time}` : '';
                    
                    const servers = d.servers || [];
                    if(favServer) servers.sort((a,b)=> a.name === favServer ? -1 : b.name === favServer ? 1 : 0);
                    
                    if(servers.length && !servers[0].name.toLowerCase().includes('vmoly') && !favServer) document.getElementById('vmolyWarning').classList.remove('hidden');
                    else document.getElementById('vmolyWarning').classList.add('hidden');

                    const sList = document.getElementById('serversList'); sList.innerHTML = '';
                    servers.forEach((s, i) => {
                        const b = document.createElement('button');
                        b.className = `btn-pill ${i===0?'active':''}`;
                        b.innerText = s.name;
                        b.onclick = () => { document.querySelectorAll('#serversList .btn-pill').forEach(x=>x.classList.remove('active')); b.classList.add('active'); favServer = s.name; localStorage.setItem('s_server', s.name); player.src = s.url; };
                        sList.appendChild(b);
                    });

                    const dList = document.getElementById('downloadsList'); dList.innerHTML = '';
                    (d.downloads || []).forEach(x => { dList.innerHTML += `<a href="${x.url}" target="_blank" class="btn-pill" style="text-decoration:none; background:var(--fg); color:var(--bg);">${x.name}</a>`; });

                    player.src = servers.length ? servers[0].url : d.video_player;
                }
            } catch(e){}
        }

        window.playNext = () => { if(epIdx < epList.length-1) fetchStream(epList[epIdx+1].id, epList[epIdx+1].title, epIdx+1); };
        window.playPrev = () => { if(epIdx > 0) fetchStream(epList[epIdx-1].id, epList[epIdx-1].title, epIdx-1); };

        function toggleWatchlist() {
            const i = watchlist.findIndex(x=>x.slug === currentAnime.slug);
            if(i > -1) watchlist.splice(i, 1); else watchlist.unshift(currentAnime);
            localStorage.setItem('s_watchlist', JSON.stringify(watchlist));
            updateWatchBtn();
        }
        function updateWatchBtn() {
            const b = document.getElementById('watchlistBtn');
            const active = watchlist.some(x=>x.slug === currentAnime.slug);
            b.innerText = active ? '[-] REMOVE WATCHLIST' : '[+] ADD WATCHLIST';
            if(active) b.classList.add('active'); else b.classList.remove('active');
        }

        function updatePlayerSandbox() {
            const p = document.getElementById('videoPlayer');
            if(document.getElementById('blockRedirects').checked) p.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-presentation allow-popups');
            else p.removeAttribute('sandbox');
        }

        document.addEventListener('click', (e) => { if (!e.target.closest('.search-container')) document.getElementById('searchResults').classList.remove('show'); });
        
        document.addEventListener('DOMContentLoaded', () => {
            updatePlayerSandbox();
            fetchHome();
        });
    </script>
</body>
</html>
"""