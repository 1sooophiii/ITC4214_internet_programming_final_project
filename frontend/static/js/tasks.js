$(document).ready(function () {
    const $submitButton = $("#taskSubmit");
    const $nameInput = $("#taskName");
    const $dateInput = $("#taskDate");
    const $descriptionInput = $("#taskDescription");

    const $taskTable = $("#taskTable");
    const $totalEl = $("#summary-total");
    const $pendingEl = $("#summary-pending");
    const $completedEl = $("#summary-completed");

    const $filterSelect = $("#filterStatus");
    const $sortSelect = $("#sortTasks");

    const $editModal = $("#editModal");
    const $editName = $("#editName");
    const $editDate = $("#editDate");
    const $editDesc = $("#editDesc");
    const $cancelEdit = $("#cancelEdit");
    const $saveEdit = $("#saveEdit");

    let editingIndex = null;
    let tasks = JSON.parse(localStorage.getItem("tasks")) || [];
    let filteredTasks = [...tasks];

    // Initial Load
    renderTasks();
    updateSummary();

    function saveTasks() {
        // save task object value as string to local storage
        localStorage.setItem("tasks", JSON.stringify(tasks));
    }

    // update task metrics
    function updateSummary() {
        $totalEl.text(tasks.length);
        $pendingEl.text(tasks.filter((t) => t.status === "Pending").length);
        $completedEl.text(tasks.filter((t) => t.status === "Completed").length);
    }

    function renderTasks() {
        // create a new html set of elements
        $taskTable.html("");

        //for each new task add a row to the table
        filteredTasks.forEach((task, index) => {
            const $row = $(`
                <tr>
                    <td class="p-3 border-b border-r box-border border-gray-300 dark:border-gray-700 max-w-[200px] overflow-x-auto whitespace-nowrap align-middle px-4">${
                        task.name
                    }</td>
                    <td class="p-3 border-b border-r box-border border-gray-300 dark:border-gray-700 max-w-[200px] overflow-x-auto whitespace-nowrap align-middle px-4">${
                        task.description
                    }</td>
                    <td class="p-3 border-b border-r box-border border-gray-300 dark:border-gray-700 max-w-[200px] overflow-x-auto whitespace-nowrap align-middle px-4">${
                        task.date
                    }</td>
                    <td class="p-3 border-b border-r box-border border-gray-300 dark:border-gray-700 max-w-[200px] overflow-x-auto whitespace-nowrap align-middle px-4">
                        <select data-index="${index}" class="status-select w-full rounded dark:text-white dark:bg-teal-700">
                            <option ${
                                task.status === "Pending" ? "selected" : ""
                            }>Pending</option>
                            <option ${
                                task.status === "Completed" ? "selected" : ""
                            }>Completed</option>
                        </select>
                    </td>
                    <td class="p-3 border-b border-r box-border border-gray-300 dark:border-gray-700 text-center max-w-[200px] overflow-x-auto whitespace-nowrap align-middle px-4">
                        <button class="edit-btn text-blue-500" data-index="${index}">Edit</button> |
                        <button class="delete-btn text-red-500" data-index="${index}">Delete</button>
                    </td>
                </tr>
            `);
            $taskTable.append($row);
        });

        feather.replace();
        bindActionEventListeners();
    }

    // when task is submitted create a new task object
    // add it to the list
    // update local storage
    $submitButton.on("click", function () {
        const newTask = {
            name: $nameInput.val().trim(),
            date: $dateInput.val(),
            description: $descriptionInput.val().trim(),
            status: "Pending",
        };

        tasks.push(newTask);
        saveTasks();
        applyFilterSort();
        updateSummary();

        //reset form
        $nameInput.val("");
        $dateInput.val("");
        $descriptionInput.val("");

        alert("Task saved!");
    });

    // Status change, edit, delete listeners
    function bindActionEventListeners() {
        $(".status-select").on("change", function () {
            const index = $(this).data("index");
            tasks[index].status = $(this).val();
            saveTasks();
            applyFilterSort();
            updateSummary();
        });

        $(".edit-btn").on("click", function () {
            editingIndex = $(this).data("index");
            const task = tasks[editingIndex];
            $editName.val(task.name);
            $editDate.val(task.date);
            $editDesc.val(task.description);
            $editModal.removeClass("hidden").addClass("flex");
        });

        $(".delete-btn").on("click", function () {
            const index = $(this).data("index");
            if (confirm("Delete this task?")) {
                // Remove 1 element from the tasks array at the specified index.
                tasks.splice(index, 1);
                saveTasks();
                applyFilterSort();
                updateSummary();
            }
        });
    }

    // Modal events
    $cancelEdit.on("click", function () {
        $editModal.addClass("hidden");
    });

    $saveEdit.on("click", function () {
        if (
            !$editName.val().trim() ||
            !$editDate.val() ||
            !$editDesc.val().trim()
        ) {
            alert("Please fill all fields.");
            return;
        }

        tasks[editingIndex] = {
            // keeping existing properties using object spread
            ...tasks[editingIndex],
            name: $editName.val().trim(),
            date: $editDate.val(),
            description: $editDesc.val().trim(),
        };

        saveTasks();
        applyFilterSort();
        updateSummary();
        $editModal.addClass("hidden");
    });

    // Filter + Sort handling
    $filterSelect.on("change", applyFilterSort);
    $sortSelect.on("change", applyFilterSort);

    function applyFilterSort() {
        const filterValue = $filterSelect.val();
        const sortValue = $sortSelect.val();

        filteredTasks = tasks.filter((task) => {
            // if filterValue is all return all items in the array tasks
            if (filterValue === "All") return true;
            // return only the items of the array that match the status value
            return task.status === filterValue;
        });

        // Sort the filteredTasks array based on sortValue:
        // by date (earliest first), by name (alphabetically), or by status (alphabetically).
        filteredTasks.sort((a, b) => {
            // - If sortValue is "date", convert both a.date and b.date to Date objects,
            //   subtract them to sort in ascending order.
            // - If sortValue is "name", use localeCompare to sort alphabetically by task name.
            // - If sortValue is "status", use localeCompare to sort alphabetically by task status.
            // - If no valid sortValue is provided, return 0 to keep original order.
            if (sortValue === "date") {
                return new Date(a.date) - new Date(b.date);
            } else if (sortValue === "name") {
                return a.name.localeCompare(b.name);
            } else if (sortValue === "status") {
                return a.status.localeCompare(b.status);
            }
            return 0;
        });

        renderTasks();
    }
});
