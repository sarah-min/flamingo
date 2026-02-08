document.addEventListener('DOMContentLoaded', () => {
    // 1. Reference the container
    const container = document.querySelector('.current-word');

    // 2. Data to populate
    const queries = ['How to fly', 'Pink feathers', 'Shrimp diet', 'Flamingo lifespan'];

    
    // 3. Loop and inject
    queries.forEach(text => {
        const queryItem = document.createElement('p');
        queryItem.textContent = text;
        queryItem.className = 'query-item';
        container.appendChild(queryItem);
    });
}); 

// document.addEventListener('DOMContentLoaded', () => {
//     // 1. Reference the container
//     const container = document.querySelector('.current-word');

//     // 2. Data to populate
//     // const queries = ['How to fly', 'Pink feathers', 'Shrimp diet', 'Flamingo lifespan'];

//     // 3. Loop and inject
//     // queries.forEach(text => {
//         const queryItem = document.createElement('p');
//         queryItem.textContent = text;
//         queryItem.className = 'query-item';
//         container.appendChild(queryItem);
//     // });
// });