async function loadDICards() {
    try {
        const [cardsDataResponse, localizationResponse] = await Promise.all([
            fetch('./data/diCards/diCards.json'),
            fetch('./data/localization/localization.en.json')
        ]);

        const cardsData = await cardsDataResponse.json();
        const localization = await localizationResponse.json();

        const container = document.getElementById('di-cards-container');

        for (const [cardId, cardInfo] of Object.entries(cardsData)) {
            const cardWrapper = document.createElement('div');
            cardWrapper.className = 'di-card-wrapper';

            // Картинка
            const imgContainer = document.createElement('div');
            imgContainer.className = 'di-card-img-container';
            const img = document.createElement('img');
            img.src = `./img/diCards/${cardId}.png`;
            img.className = 'di-card-img';
            imgContainer.appendChild(img);
            cardWrapper.appendChild(imgContainer);

            // Информация справа
            const infoContainer = document.createElement('div');
            infoContainer.className = 'di-card-info';

            // Название
            const titleText = localization[cardInfo.name] || cardInfo.name;
            const titleElement = document.createElement('div');
            titleElement.className = 'di-card-title';
            titleElement.textContent = titleText;
            infoContainer.appendChild(titleElement);

            // Основные параметры (cost, count, icon, taSeti)
            const metaContainer = document.createElement('div');
            metaContainer.className = 'di-card-meta';
            
            const costText = `Cost: ${cardInfo.cost}`;
            const countText = `Count: ${cardInfo.count}`;
            const iconKey = `icon.${cardInfo.icon}`;
            const iconName = localization[iconKey] || cardInfo.icon;
            const iconText = `Type: ${iconName}`;
            const taSetiText = cardInfo.taSeti ? 'Ta-Seti: Yes' : 'Ta-Seti: No';

            metaContainer.innerHTML = `
                <span>${costText}</span> | 
                <span>${countText}</span> | 
                <span>${iconText}</span> | 
                <span>${taSetiText}</span>
            `;
            infoContainer.appendChild(metaContainer);

            // Текст
            const textContent = localization[cardInfo.text] || cardInfo.text;
            const textElement = document.createElement('div');
            textElement.className = 'di-card-text';
            textElement.innerHTML = textContent.replace(/☥/g, '<span class="kemet-symbol-ankh">☥</span>');
            infoContainer.appendChild(textElement);

            cardWrapper.appendChild(infoContainer);
            container.appendChild(cardWrapper);
        }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadDICards);
