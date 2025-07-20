$(document).ready(function () {
    const $studioForm = $("#studioForm");
    const $songTitle = $("#songTitle");
    const $songNotes = $("#songNotes");
    const $keySelect = $("#key-select");
    const $moodButtons = $(
        ".bg-blue-500, .bg-yellow-500, .bg-red-500, .bg-purple-500"
    );
    let selectedMood = "";

    // Diatonic chords for each key
    const keyChords = {
        "C Major": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
        "C♯/D♭ Major": ["C♯", "D♯m", "E♯m", "F♯", "G♯", "A♯m", "B♯dim"],
        "D Major": ["D", "Em", "F♯m", "G", "A", "Bm", "C♯dim"],
        "D♯/E♭ Major": ["E♭", "Fm", "Gm", "A♭", "B♭", "Cm", "Ddim"],
        "E Major": ["E", "F♯m", "G♯m", "A", "B", "C♯m", "D♯dim"],
        "F Major": ["F", "Gm", "Am", "B♭", "C", "Dm", "Edim"],
        "F♯/G♭ Major": ["F♯", "G♯m", "A♯m", "B", "C♯", "D♯m", "E♯dim"],
        "G Major": ["G", "Am", "Bm", "C", "D", "Em", "F♯dim"],
        "G♯/A♭ Major": ["A♭", "B♭m", "Cm", "D♭", "E♭", "Fm", "Gdim"],
        "A Major": ["A", "Bm", "C♯m", "D", "E", "F♯m", "G♯dim"],
        "A♯/B♭ Major": ["B♭", "Cm", "Dm", "E♭", "F", "Gm", "Adim"],
        "B Major": ["B", "C♯m", "D♯m", "E", "F♯", "G♯m", "A♯dim"],

        "A Minor": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
        "A♯/B♭ Minor": ["A♯m", "Cdim", "C♯", "D♯m", "Fm", "F♯", "G♯"],
        "B Minor": ["Bm", "C♯dim", "D", "Em", "F♯m", "G", "A"],
        "C Minor": ["Cm", "Ddim", "E♭", "Fm", "Gm", "A♭", "B♭"],
        "C♯/D♭ Minor": ["C♯m", "D♯dim", "E", "F♯m", "G♯m", "A", "B"],
        "D Minor": ["Dm", "Edim", "F", "Gm", "Am", "B♭", "C"],
        "D♯/E♭ Minor": ["D♯m", "Fdim", "F♯", "G♯m", "A♯m", "B", "C♯"],
        "E Minor": ["Em", "F♯dim", "G", "Am", "Bm", "C", "D"],
        "F Minor": ["Fm", "Gdim", "A♭", "B♭m", "Cm", "D♭", "E♭"],
        "F♯/G♭ Minor": ["F♯m", "G♯dim", "A", "Bm", "C♯m", "D", "E"],
        "G Minor": ["Gm", "Adim", "B♭", "Cm", "Dm", "E♭", "F"],
        "G♯/A♭ Minor": ["G♯m", "A♯dim", "B", "C♯m", "D♯m", "E", "F♯"],
    };

    // Example progressions using chord indices
    const progressionTemplates = [
        [0, 3, 4, 0], // I - IV - V - I
        [5, 3, 0, 4], // vi - IV - I - V
        [1, 4, 0], // ii - V - I
        [0, 5, 1, 4], // I - vi - ii - V
        [0, 4, 5, 3], // I - V - vi - IV
    ];

    function updateChordSuggestions(selectedKey) {
        const chords = keyChords[selectedKey];
        const $suggestionList = $("#chord-suggestions");
        $suggestionList.empty();

        if (!chords) {
            $suggestionList.html("<li>No chords available for this key.</li>");
            return;
        }

        // For each progression template, map index values to chord names,
        // join them into a string, create an <li> element with the key and progression,
        // then append it to the suggestion list in the DOM.
        progressionTemplates.forEach((progression, idx) => {
            const chordProgression = progression
                // creates a new array by applying a function to each element of the original array
                .map((i) => chords[i])
                .join(" - ");
            const $li = $("<li>").text(`${selectedKey}: ${chordProgression}`);
            $suggestionList.append($li);
        });
    }

    // Attach event listener
    $keySelect.on("change", function () {
        const selected = $(this).val();
        if (selected && selected !== "Select a key") {
            updateChordSuggestions(selected);
        }
    });

    // Mood selection handler
    $moodButtons.on("click", function (e) {
        e.preventDefault();
        selectedMood = $(this).text().trim();

        // visually mark the selected one
        $moodButtons.removeClass("ring ring-offset-2");
        $(this).addClass("ring ring-offset-2");
    });

    $studioForm.on("submit", function (e) {
        e.preventDefault();

        const selectedKey = $keySelect.val();

        // Get selected instruments
        const instrumentCheckboxes = $studioForm.find('input[type="checkbox"]');

        // filter only the checked ones,
        // map to the label text (parent element's text),
        // trim whitespace, and join all selected instrument names with commas.
        const selectedInstruments = instrumentCheckboxes
            .filter(":checked")
            .map(function () {
                return $(this).parent().text().trim();
            })
            .get()
            .join(", ");

        // Generate chord progressions
        const chords = keyChords[selectedKey];
        let progressionText = "No progressions available.";

        if (chords) {
            const progressions = progressionTemplates.map((pattern) =>
                pattern.map((i) => chords[i]).join(" - ")
            );
            progressionText = progressions
                .map((p, idx) => `  ${idx + 1}. ${p}`)
                .join("\n");
        }

        // Compose rich description with chord progressions
        const descriptionParts = [
            `Key: ${selectedKey}`,
            `Suggested Progressions:\n${progressionText}`,
            `Mood: ${selectedMood || "Not selected"}`,
            `Instruments: ${selectedInstruments || "None"}`,
            `Notes: ${$songNotes.val().trim() || "No notes provided"}`,
        ];
        const fullDescription = descriptionParts.join("\n\n");

        const newTask = {
            name: $songTitle.val() || "Untitled Song Idea",
            description: fullDescription,
            date: new Date().toISOString().split("T")[0],
            status: "Pending",
            source: "studio",
        };

        // Save to localStorage
        const existing = JSON.parse(localStorage.getItem("tasks")) || [];
        existing.push(newTask);
        localStorage.setItem("tasks", JSON.stringify(existing));

        // Reset form fields
        $songTitle.val("");
        $songNotes.val("");
        $keySelect.prop("selectedIndex", 0);
        instrumentCheckboxes.prop("checked", false);
        selectedMood = "";
        $moodButtons.removeClass("ring ring-offset-2");
        $("#chord-suggestions").empty();

        alert("Song saved as task!");
    });
});
