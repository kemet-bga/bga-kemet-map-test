// Загрузка данных и отображение тайлов силы
async function loadPowerTiles() {
    try {
        // Загружаем все JSON файлы параллельно
        const [layoutResponse, spritesheetResponse, tilesDataResponse, localizationResponse] = await Promise.all([
            fetch('./data/powerTiles/powerTilesLayout.json'),
            fetch('./img/powerTiles/powerTiles.json'),
            fetch('./data/powerTiles/powerTiles.json'),
            fetch('./data/localization/localization.en.json')
        ]);

        const layout = await layoutResponse.json();
        const spritesheet = await spritesheetResponse.json();
        const tilesData = await tilesDataResponse.json();
        const localization = await localizationResponse.json();

        const container = document.getElementById('power-tiles-container');

        // Обрабатываем каждую группу (ruby, sapphire, diamond, onyx)
        for (const [groupKey, groupData] of Object.entries(layout)) {
            // Создаем секцию для группы
            const section = document.createElement('div');
            section.className = 'power-tiles-section';

            // Создаем заголовок группы с цветом
            const title = document.createElement('h2');
            title.textContent = groupData.title;
            title.style.color = `#${groupData.titleColor}`;
            section.appendChild(title);

            // Создаем сетку 4x4
            const grid = document.createElement('div');
            grid.className = 'power-tiles-grid';

            // Заполняем сетку тайлами
            groupData.layout.forEach(row => {
                row.forEach(tileName => {
                    const tileWrapper = document.createElement('div');
                    tileWrapper.className = 'power-tile-wrapper';

                    const tileDiv = document.createElement('div');
                    tileDiv.className = 'power-tile';

                    // Получаем координаты из spritesheet
                    const frameData = spritesheet.frames[tileName];
                    if (frameData) {
                        const { x, y, w, h } = frameData.frame;

                        // Устанавливаем background-image и позиционирование
                        tileDiv.style.backgroundImage = 'url(./img/powerTiles/powerTiles.jpg)';
                        tileDiv.style.backgroundPosition = `-${x}px -${y}px`;
                        tileDiv.style.width = `${w}px`;
                        tileDiv.style.height = `${h}px`;
                    }

                    tileWrapper.appendChild(tileDiv);

                    // Получаем данные тайла
                    const tileInfo = tilesData[tileName];
                    if (tileInfo) {
                        // Получаем локализованное название
                        const titleKey = tileInfo.name;
                        const titleText = localization[titleKey] || titleKey;

                        const titleElement = document.createElement('div');
                        titleElement.className = 'power-tile-title';
                        titleElement.textContent = titleText;

                        // Устанавливаем цвет заголовка в зависимости от группы
                        const group = tileInfo.group;
                        if (group && layout[group]) {
                            titleElement.style.color = `#${layout[group].titleColor}`;
                        }

                        tileWrapper.appendChild(titleElement);

                        // Получаем локализованный текст
                        const textKey = tileInfo.text;
                        const textContent = localization[textKey] || textKey;

                        const textElement = document.createElement('div');
                        textElement.className = 'power-tile-text';
                        textElement.style.textAlign = 'left';
                        textElement.style.whiteSpace = 'pre-line';
                        textElement.innerHTML = textContent.replace(/☥/g, '<span class="kemet-symbol-ankh">☥</span>');
                        tileWrapper.appendChild(textElement);

                        // Добавляем action token если есть
                        if (tileInfo.silverActionToken) {
                            const tokenImg = document.createElement('img');
                            tokenImg.src = './img/actionTokens/silver.png';
                            tokenImg.className = 'action-token-img';
                            tileWrapper.appendChild(tokenImg);
                        } else if (tileInfo.goldActionToken) {
                            const tokenImg = document.createElement('img');
                            tokenImg.src = './img/actionTokens/gold.png';
                            tokenImg.className = 'action-token-img';
                            tileWrapper.appendChild(tokenImg);
                        }

                        // Добавляем creature если есть
                        if (tileInfo.creature) {
                            const creatureImg = document.createElement('img');
                            creatureImg.src = `./img/creatures/${tileInfo.creature}.png`;
                            creatureImg.className = 'action-token-img';
                            tileWrapper.appendChild(creatureImg);
                        }
                    }

                    grid.appendChild(tileWrapper);
                });
            });

            section.appendChild(grid);
            container.appendChild(section);
        }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

// Запускаем загрузку при загрузке страницы
document.addEventListener('DOMContentLoaded', loadPowerTiles);
