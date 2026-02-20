import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    with open('calculator.html', 'r', encoding='utf-8') as f:
        calc = f.read()

    # Shared Button
    btn_html = '''\n<button id="lang-toggle" onclick="toggleLang()" class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-3 py-1.5 rounded-lg text-sm font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-sm ml-2 md:ml-4"><span class="material-symbols-outlined text-sm">translate</span><span id="lang-label">KO</span></button>'''

    # --- index.html ---
    idx = idx.replace('Sign In\n                    </button>', f'Sign In\n                    </button>{btn_html}')
    # Add to mobile menu as well
    idx = idx.replace('<div class="md:hidden">', f'<div class="flex items-center gap-2 md:hidden">{btn_html}<div class="md:hidden">')
    idx = idx.replace('href="#"', 'href="javascript:void(alert(\'준비 중인 기능입니다. (Coming soon)\'))"')
    # City Links (first href="calculator.html" in the main button remains bali? No, let's keep it as bali)
    idx = idx.replace('href="calculator.html"', 'href="calculator.html?city=bali"')
    # Features links update
    idx = idx.replace('href="calculator.html?city=bali"\n<!-- City Card 2 -->', 'href="calculator.html?city=bali"\n<!-- City Card 2 -->')
    idx = idx.replace('<!-- City Card 1 -->\n<a class="block', '<!-- City Card 1 -->\n<a href="calculator.html?city=lisbon" class="block')
    idx = idx.replace('<!-- City Card 3 -->\n<a class="block', '<!-- City Card 3 -->\n<a href="calculator.html?city=chiangmai" class="block')
    # Popular Tags fixes
    idx = idx.replace('<a class="flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-slate-200/50 dark:bg-slate-800 hover:bg-primary/10 hover:text-primary transition-all text-sm font-medium" href="javascript:void(alert(\'준비 중인 기능입니다. (Coming soon)\'))">\n<span class="material-symbols-outlined text-sm">location_on</span> Bali',
                      '<a class="flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-slate-200/50 dark:bg-slate-800 hover:bg-primary/10 hover:text-primary transition-all text-sm font-medium" href="calculator.html?city=bali">\n<span class="material-symbols-outlined text-sm">location_on</span> Bali')
    idx = idx.replace('<span class="material-symbols-outlined text-sm">location_on</span> Chiang Mai',
                      '<span class="material-symbols-outlined text-sm">location_on</span> Chiang Mai</a>') # Adjust if broken
    # For tags, let's just forcefully fix them
    idx = re.sub(r'<a.*?href="(?!calculator).*?>\s*<span.*?location_on</span> (Bali|Chiang Mai|Lisbon|Medellín)\s*</a>', 
                 lambda m: f'<a class="flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-slate-200/50 dark:bg-slate-800 hover:bg-primary/10 hover:text-primary transition-all text-sm font-medium" href="calculator.html?city={m.group(1).lower().replace(" ", "").replace("í", "i")}">\n<span class="material-symbols-outlined text-sm">location_on</span> {m.group(1)}\n</a>', idx)

    # --- calculator.html ---
    calc = calc.replace('class="hidden sm:flex items-center gap-2 px-4 py-2 text-sm font-medium border border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"',
                        'id="lang-toggle" onclick="toggleLang()" class="sm:flex items-center gap-2 px-4 py-2 text-sm font-bold border border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"')
    calc = calc.replace('<span class="material-symbols-outlined text-lg">language</span> USD', '<span class="material-symbols-outlined text-lg">translate</span> <span id="lang-label">KO</span>')
    calc = calc.replace('href="#"', 'href="javascript:void(alert(\'기능이 곧 추가됩니다. (Coming soon)\'))"')
    
    # Enable adding ID for elements we change dynamically
    calc = calc.replace('Gojek/Grab', '<span id="taxi-label">Gojek/Grab</span>')
    calc = calc.replace('Local Warungs (%)', '<span id="local-warung-label">Local Warungs (%)</span>')

    i18n_script = """
<script>
const dict = {
    "Explore": "탐색", "Community": "커뮤니티", "Pricing": "비용 정보", "Sign In": "로그인",
    "Discover the world's best cities for digital nomads. We rank places based on cost, internet speed, safety, and quality of life.": "디지털 노마드를 위한 최고의 도시를 발견하세요. 물가, 인터넷 속도, 안전 및 삶의 질을 기반으로 순위를 확인합니다.",
    "Search": "검색", "Popular:": "인기 도시:", "Gigabit Internet": "기가비트 인터넷", "Available in 450+ cities": "450여 개 도시에서 이용 가능",
    "Cities Indexed": "등록된 도시 수", "Nomad Reviews": "리뷰(건)", "Avg. Wi-Fi Speed": "평균 Wi-Fi 속도", "Avg. Living Cost": "평균 생활비",
    "Featured Destinations": "추천 목적지", "Hand-picked locations with the best balance of cost and lifestyle.": "비용과 라이프스타일 밸런스가 뛰어난 엄선된 도시별 정보.",
    "View all cities": "모든 도시 보기", "Lisbon, Portugal": "포르투갈, 리스본", "Coastal City • Tech Hub": "해안 도시 • 테크 허브",
    "per month": "월 기준", "High": "높음", "Bali, Indonesia": "인도네시아, 발리", "Island • Coworking Paradise": "휴양지 • 코워킹 천국",
    "Chiang Mai, Thailand": "태국, 치앙마이", "Mountainous • Low Cost": "산악 지대 • 저렴한 물가", "Very Safe": "매우 안전함",
    "Ready to find your next home?": "다음 도시를 찾을 준비가 되셨나요?", "Join 50,000+ digital nomads and get access to exclusive city reports, community forums, and remote job listings.": "5만 명 이상의 노마드 커뮤니티에 참여하고 리포트와 채용 정보를 확인하세요.",
    "Join the Community": "커뮤니티 가입", "Browse All Cities": "모든 도시 살펴보기", "Product": "서비스", "Nomad Score": "노마드 스코어",
    "API": "API", "Resources": "리소스", "Blog": "블로그", "Remote Jobs": "원격 채용", "Guides": "도시 가이드", "Company": "회사",
    "About": "소개", "Careers": "채용 정보", "Privacy": "개인정보 보호", "Terms": "이용 약관",
    "NomadBudget": "노마드예산", "Destinations": "목적지", "Compare": "비교", "Save Plan": "계획 저장", "Bali Monthly Cost": "발리 예상 생활비",
    "Plan your digital nomad lifestyle in Bali. Adjust the sliders below to get a personalized estimate of your monthly expenses.": "자신의 라이프스타일에 맞게 슬라이더를 조정하여 예상 월별 지출액을 확인하세요.",
    "Indonesia": "인도네시아", "Estimated Monthly Total": "예상 월별 총 예산", "/ month": "/ 월", "Rent & Accommodation": "임대 및 숙박",
    "Accommodation Type": "숙소 유형", "Shared Villa": "공유 빌라/게스트하우스", "Private Studio": "프라이빗 스튜디오 (원룸)", "Luxury Hotel": "럭셔리 호텔",
    "Monthly Rent Budget": "월간 렌트 예산", "Food & Dining": "식사 및 다이닝", 
    "Avg. meal price": "평균 식비 (1끼)", "Coffee/Drinks": "커피/음료비", "Monthly Food Total": "월 식사 비용",
    "Transportation": "교통 수단", "Scooter Rental": "스쿠터 렌탈/대여", "Workspace": "업무 공간",
    "Unlimited Coworking Pass ($180)": "무제한 코워킹 패스 ($180)", "10-Day Pass ($90)": "10일권 패스 ($90)", "Home Office Only ($0)": "재택 근무 전용 ($0)", "Cafe Hopping ($150)": "카페 호핑 ($150)", 
    "Popular hubs: Outpost, Tropical Nomad, BWork.": "인기 코워킹 스페이스: 아웃포스트, 뷰워크 등.", "Expense Breakdown": "예산 상세 내역", " Rent": " 숙소",
    " Food": " 식비", " Transport": " 교통", " Others": " 기타", "Compare with City": "다른 도시와 비교해보기", "Chiang Mai Estimate": "타 도시 예상 비용",
    "Share this Budget": "예산 정보 공유하기", "Lifestyle & Activities": "라이프스타일 및 엑티비티",
    "Surfing": "서핑 등 액티비티", "Rental + Lessons": "장비 대여 + 강습", "Yoga Pass": "요가/피트니스 통행권", "Unlimited Monthly": "한 달 무제한 이용권",
    "Nightlife": "나이트라이프/클럽", "Beach Clubs & Bars": "비치클럽 & 바", "Add Activity": "직접 추가하기", "Bali Guide": "도시 핵심 가이드",
    "Internet Speed": "평균 와이파이 속도", "Avg. 45Mbps fiber": "약 45Mbps에서 100Mbps", "Best Time to Visit": "방문 권장 시기", "May - September": "건기 시즌 분기",
    "Safety Rating": "안전 지수", "High (Expat friendly)": "안전 (외국인 커뮤니티 활성화)", "Read full destination guide ": "더 자세한 정보 알아보기(링크) ",
    "Helping digital nomads plan their next adventure with real-time cost of living data and budgeting tools.": "정확하고 리얼한 물가 비용 도구를 활용해 다음 여행의 걱정 없이 떠나세요.",
    "Platform": "플랫폼", "Calculators": "비용 계산기", "Comparison": "생활비 비교", "Nomad List": "노마드 랭킹", "Visa Guide": "비자 및 체류 정보",
    "Travel Insurance": "유학생/여행자 보험", "Connect": "소통 채널", "Privacy Policy": "개인정보 보호", "Terms of Service": "이용 약관",
    "Lisbon Monthly Cost": "리스본 예상 생활비", "Chiang Mai Monthly Cost": "치앙마이 예상 생활비",
    "Portugal": "포르투갈", "Thailand": "태국"
};

function applyTranslations(node) {
    if (node.nodeType === 3) {
        let text = node.nodeValue.trim();
        // Exact match
        if (dict[text]) {
            node.nodeValue = node.nodeValue.replace(text, dict[text]);
        } else {
            // Check substrings for multi-part words
            for(let key in dict) {
                if (text === key) {
                    node.nodeValue = node.nodeValue.replace(key, dict[key]);
                }
            }
            if (text.includes("Work from ")) node.nodeValue = node.nodeValue.replace("Work from ", "자유롭게 거주하며 ");
            if (text.includes("anywhere.")) node.nodeValue = node.nodeValue.replace("anywhere.", "어디서든 일하세요.");
        }
    } else if (node.nodeType === 1) {
        if (node.tagName === 'INPUT' && node.placeholder && dict[node.placeholder]) {
            node.placeholder = dict[node.placeholder];
        }
        for (let child of node.childNodes) {
            applyTranslations(child);
        }
    }
}

function initLang() {
    const isKo = localStorage.getItem('lang') === 'ko';
    document.documentElement.lang = isKo ? 'ko' : 'en';
    const l1 = document.getElementById('lang-label');
    if(l1) l1.textContent = isKo ? 'EN' : 'KO';
    
    // special handling for multiple nav
    const ls = document.querySelectorAll('#lang-label');
    ls.forEach(l => l.textContent = isKo ? 'EN' : 'KO');

    if(isKo) {
        applyTranslations(document.body);
    }
}

window.toggleLang = function() {
    const cur = localStorage.getItem('lang');
    localStorage.setItem('lang', cur === 'ko' ? 'en' : 'ko');
    location.reload();
}

// Call on ready not immediate to avoid parse blocking and missing elements
window.addEventListener('DOMContentLoaded', initLang);
</script>
"""

    city_dynamic_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const city = params.get('city') || 'bali';
    
    const cityTitle = document.querySelector('h1');
    const cityGuideTitle = document.querySelector('h3.text-2xl.font-bold.mb-4');
    const bCity = document.querySelectorAll('nav span.text-slate-900.dark\\\\:text-slate-100')[0] || document.querySelector('nav span'); // fallback
    const bCountry = document.querySelectorAll('nav a.hover\\\\:text-primary')[1];
    const heroImage = document.querySelector('img[data-location]');
    const rentSlider = document.getElementById('rent-slider');
    
    let isKo = localStorage.getItem('lang') === 'ko';

    if (city === 'lisbon') {
        if(cityTitle) cityTitle.textContent = isKo ? "리스본 예상 생활비" : "Lisbon Monthly Cost";
        if(cityGuideTitle) cityGuideTitle.textContent = isKo ? "리스본 가이드" : "Lisbon Guide";
        if(bCity) bCity.textContent = isKo ? "리스본" : "Lisbon";
        if(bCountry) bCountry.textContent = isKo ? "포르투갈" : "Portugal";
        if(heroImage) heroImage.src = "https://lh3.googleusercontent.com/aida-public/AB6AXuDQ4LhsVzOjc6zvAHNjGBjWkeSsEWHSHYcngRHORW1plQCuXe91FPt-oUzT8RtznR38j6sb4MgBPa4HigrcCJx_sn3TiVAFuZVXQZ01cFwqIlhFup5e_eDkeNIaRnyYyhd1IU82Q67mAQA7xCBJd_Izh1mbHuC9AgcQQ7C6I7rfEiVqB3IpSTbxVCuwZlWyHuG087U7pMoWitF9Zn95IWaWWQoT9nYx2F9h6gYqaaye_la9sKxK3LQrMGSV_1qZBFZDVyKji6pFwVD_";
        if(rentSlider) { rentSlider.value = 1400; rentSlider.dispatchEvent(new Event('input')); }
        
        let labelw = document.getElementById('local-warung-label');
        if(labelw) labelw.textContent = isKo ? "로컬 타스카 비율(%)" : "Local Tascas (%)";
        
        let tx = document.getElementById('taxi-label');
        if(tx) tx.textContent = "Uber/Bolt";
    } 
    else if (city === 'chiangmai') {
        if(cityTitle) cityTitle.textContent = isKo ? "치앙마이 예상 생활비" : "Chiang Mai Monthly Cost";
        if(cityGuideTitle) cityGuideTitle.textContent = isKo ? "치앙마이 안내" : "Chiang Mai Guide";
        if(bCity) bCity.textContent = isKo ? "치앙마이" : "Chiang Mai";
        if(bCountry) bCountry.textContent = isKo ? "태국" : "Thailand";
        if(heroImage) heroImage.src = "https://lh3.googleusercontent.com/aida-public/AB6AXuD6Cgu-xRJnBrxeA0Yt4o1SS4MbdFCAMolnl_WcrVHyozxlYrG022WTRh2GBIJVBB_tSlGY9LNeGuqoSejjilNTK9FNtgZExxhrOoZ0KUBur0KdFjJ_gB3IRAgG3a_fPIssv00ElTtlEmYeEUhOssODzORj-wZF5JjXIvkMxFqPiqF6zsZhLi1pE4PdSxMf7qWE4plxXubCOXhRI12nJE1bMNJh18FKEIi_P7uNr39Sw0KtfKI-L5grqQpAn7GtLmCZkrdjADrmgwEN";
        if(rentSlider) { rentSlider.value = 450; rentSlider.dispatchEvent(new Event('input')); }
        
        let labelw = document.getElementById('local-warung-label');
        if(labelw) labelw.textContent = isKo ? "로컬 식당 비율(%)": "Local Street Food (%)";
        let tx = document.getElementById('taxi-label');
        if(tx) tx.textContent = "Grab/TukTuk";
    } else {
         if(cityTitle && isKo) cityTitle.textContent = "발리 예상 생활비";
         if(bCity && isKo) bCity.textContent = "발리";
         if(bCountry && isKo) bCountry.textContent = "인도네시아";
    }
});
</script>
"""

    idx = idx.replace('</body>', i18n_script + '\n</body>')
    calc = calc.replace('</body>', i18n_script + '\n' + city_dynamic_script + '\n</body>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    with open('calculator.html', 'w', encoding='utf-8') as f:
        f.write(calc)

main()
