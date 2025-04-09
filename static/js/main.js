// Main JavaScript file for SESAME Academic

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any components that need JavaScript
    initializeTooltips();
    initializeDropdowns();
    setupAPIFetching();
});

// Initialize tooltips
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'absolute bg-gray-800 text-white text-sm rounded py-1 px-2 -mt-8 z-10';
            tooltipEl.textContent = tooltipText;
            this.appendChild(tooltipEl);
        });

        tooltip.addEventListener('mouseleave', function() {
            const tooltipEl = this.querySelector('div');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });
}

// Initialize dropdown menus
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        const content = dropdown.querySelector('.dropdown-content');

        if (trigger && content) {
            trigger.addEventListener('click', function() {
                content.classList.toggle('hidden');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!dropdown.contains(event.target)) {
                    content.classList.add('hidden');
                }
            });
        }
    });
}

// Setup API fetching for dynamic content
function setupAPIFetching() {
    // Fetch data from API endpoints when needed
    const apiElements = document.querySelectorAll('[data-api-endpoint]');

    apiElements.forEach(element => {
        const endpoint = element.getAttribute('data-api-endpoint');

        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                // Handle different types of data
                if (element.classList.contains('api-list')) {
                    renderList(element, data);
                } else if (element.classList.contains('api-chart')) {
                    renderChart(element, data);
                } else if (element.classList.contains('api-form')) {
                    populateForm(element, data);
                } else {
                    element.textContent = JSON.stringify(data, null, 2);
                }
            })
            .catch(error => {
                console.error('Error fetching API data:', error);
                element.innerHTML = `<div class="text-red-500">Error loading data</div>`;
            });
    });
}

// Render a list from API data
function renderList(element, data) {
    // Check if data has indicators array (for LCA metadata)
    if (data && data.indicators && Array.isArray(data.indicators)) {
        const ul = document.createElement('ul');
        ul.className = 'divide-y divide-gray-200';

        data.indicators.forEach(item => {
            const li = document.createElement('li');
            li.className = 'py-3 px-4 flex justify-between items-center';

            const labelSpan = document.createElement('span');
            labelSpan.className = 'font-medium text-gray-700';
            labelSpan.textContent = item.label;

            const valueSpan = document.createElement('span');
            valueSpan.className = 'text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded';
            valueSpan.textContent = item.value;

            li.appendChild(labelSpan);
            li.appendChild(valueSpan);
            ul.appendChild(li);
        });

        element.innerHTML = '';
        element.appendChild(ul);
    }
    // Check if data has analyses array (for TEA metadata)
    else if (data && data.analyses && Array.isArray(data.analyses)) {
        const ul = document.createElement('ul');
        ul.className = 'divide-y divide-gray-200';

        data.analyses.forEach(item => {
            const li = document.createElement('li');
            li.className = 'py-4 px-4';

            const nameDiv = document.createElement('div');
            nameDiv.className = 'flex justify-between items-center mb-2';

            const nameSpan = document.createElement('span');
            nameSpan.className = 'font-medium text-lg text-green-700';
            nameSpan.textContent = item.name;

            const unitSpan = document.createElement('span');
            unitSpan.className = 'text-sm bg-green-100 text-green-800 px-2 py-1 rounded';
            unitSpan.textContent = item.unit;

            nameDiv.appendChild(nameSpan);
            nameDiv.appendChild(unitSpan);

            const pathwayDiv = document.createElement('div');
            pathwayDiv.className = 'text-sm text-gray-600 mb-2';
            pathwayDiv.textContent = 'Pathway: ' + item.pathway_id.join(' → ');

            const inputsDiv = document.createElement('div');
            inputsDiv.className = 'text-xs text-gray-500';
            inputsDiv.textContent = `${item.user_inputs?.length || 0} configurable parameters`;

            li.appendChild(nameDiv);
            li.appendChild(pathwayDiv);
            li.appendChild(inputsDiv);
            ul.appendChild(li);
        });

        element.innerHTML = '';
        element.appendChild(ul);
    }
    // Check if data is an array (for other endpoints)
    else if (Array.isArray(data)) {
        const ul = document.createElement('ul');
        ul.className = 'divide-y divide-gray-200';

        data.forEach(item => {
            const li = document.createElement('li');
            li.className = 'py-3 px-4';
            li.textContent = item.name || item.label || item.value || JSON.stringify(item);
            ul.appendChild(li);
        });

        element.innerHTML = '';
        element.appendChild(ul);
    }
    // For pathway stages or other structured data
    else if (data && data.stages && Array.isArray(data.stages)) {
        const div = document.createElement('div');
        div.className = 'space-y-2';

        const stagesCount = Math.min(data.stages.length, 5); // Limit to first 5 stages for brevity

        for (let i = 0; i < stagesCount; i++) {
            const stage = data.stages[i];
            const stageDiv = document.createElement('div');
            stageDiv.className = 'bg-gray-50 p-3 rounded border';
            stageDiv.innerHTML = `<span class="font-medium">${stage.name}</span> <span class="text-sm text-gray-500">(${stage.id})</span>`;
            div.appendChild(stageDiv);
        }

        if (data.stages.length > 5) {
            const moreDiv = document.createElement('div');
            moreDiv.className = 'text-center text-sm text-gray-500 mt-2';
            moreDiv.textContent = `+ ${data.stages.length - 5} more stages`;
            div.appendChild(moreDiv);
        }

        element.innerHTML = '';
        element.appendChild(div);
    }
    // Default fallback for other data structures
    else {
        const pre = document.createElement('pre');
        pre.className = 'text-xs overflow-auto bg-gray-50 p-3 rounded';
        pre.textContent = JSON.stringify(data, null, 2);

        element.innerHTML = '';
        element.appendChild(pre);
    }
}

// Render a chart from API data (placeholder - would use a chart library in production)
function renderChart(element, data) {
    element.innerHTML = `<div class="p-4 border rounded bg-gray-50">
        <p class="text-center text-gray-500">Chart would render here with the provided data</p>
        <pre class="mt-4 text-xs overflow-auto">${JSON.stringify(data, null, 2)}</pre>
    </div>`;
}

// Populate a form with API data
function populateForm(element, data) {
    if (data.user_inputs) {
        const form = document.createElement('form');
        form.className = 'space-y-4';

        data.user_inputs.forEach(input => {
            const formGroup = document.createElement('div');

            const label = document.createElement('label');
            label.className = 'form-label';
            label.textContent = input.label;

            let inputElement;

            if (input.type === 'categorical' || input.type === 'options') {
                inputElement = document.createElement('select');
                inputElement.className = 'form-select';

                // Add options
                const options = input.options || [];
                options.forEach(option => {
                    const optionEl = document.createElement('option');
                    optionEl.value = option.value;
                    optionEl.textContent = option.value;
                    inputElement.appendChild(optionEl);
                });

                // Add default option if no options provided
                if (options.length === 0) {
                    const defaultOption = document.createElement('option');
                    defaultOption.value = input.defaults?.[0]?.value || '';
                    defaultOption.textContent = input.defaults?.[0]?.value || 'Select an option';
                    inputElement.appendChild(defaultOption);
                }
            } else {
                inputElement = document.createElement('input');
                inputElement.className = 'form-input';
                inputElement.type = input.type === 'continuous' ? 'number' : 'text';
                inputElement.value = input.defaults?.[0]?.value || '';

                if (input.unit) {
                    const inputGroup = document.createElement('div');
                    inputGroup.className = 'flex items-center';

                    inputGroup.appendChild(inputElement);

                    const unitSpan = document.createElement('span');
                    unitSpan.className = 'ml-2 text-gray-500';
                    unitSpan.textContent = input.unit;

                    inputGroup.appendChild(unitSpan);
                    formGroup.appendChild(label);
                    formGroup.appendChild(inputGroup);
                    form.appendChild(formGroup);
                    return;
                }
            }

            formGroup.appendChild(label);
            formGroup.appendChild(inputElement);

            if (input.tooltip) {
                const tooltipIcon = document.createElement('span');
                tooltipIcon.className = 'ml-1 text-gray-400 cursor-help';
                tooltipIcon.textContent = 'ⓘ';
                tooltipIcon.setAttribute('data-tooltip', input.tooltip.content || input.tooltip);
                label.appendChild(tooltipIcon);
            }

            form.appendChild(formGroup);
        });

        const submitButton = document.createElement('button');
        submitButton.className = 'btn-primary';
        submitButton.type = 'submit';
        submitButton.textContent = 'Submit';

        form.appendChild(submitButton);

        element.innerHTML = '';
        element.appendChild(form);
    } else {
        element.textContent = JSON.stringify(data, null, 2);
    }
}
