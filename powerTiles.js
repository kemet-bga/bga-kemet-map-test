// Загрузка данных и отображение тайлов силы
async function loadPowerTiles() {
    try {
        // Загружаем оба JSON файла параллельно
        const [layoutResponse, spritesheetResponse] = await Promise.all([
            fetch('./data/powerTiles/powerTilesLayout.json'),
            fetch('./img/powerTiles/powerTiles.json')
        ]);

        const layout = await layoutResponse.json();
        const spritesheet = await spritesheetResponse.json();

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

                    grid.appendChild(tileDiv);
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
