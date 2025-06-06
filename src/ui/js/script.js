document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const queryInput = document.getElementById("search-bar");
    const limitSelect = document.getElementById("limit");
    const submitButton = form.querySelector("button[type=\"submit\"]");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const query = queryInput.value.trim();
        const limit = parseInt(limitSelect.value, 10);

        // Prevent multiple calls.
        submitButton.disabled = true;
        console.log(`Called: ${query} with a max result limit of: ${limit}`);

        // Hide the pre-text and show the mid-text spinner.
        const preTextElement = document.getElementById("pre-text");
        const midTextElement = document.getElementById("mid-text");

        preTextElement.classList.remove("not-hidden");
        preTextElement.classList.add("hidden");

        midTextElement.classList.remove("hidden");
        midTextElement.classList.add("not-hidden");

        console.log("Loader displayed");

        fetch(`/ask?limit=${limit}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        })
            .then(res => res.json())
            .then(data => processResponse(data))
            .catch(err => {
                console.error(err)
                window.alert("Error occurred in fetching details, please try again or file an issue!");
            })
            .finally(() => submitButton.disabled = false);

        // For now, immediately re-enable button
        submitButton.disabled = false;
    });

    const scrollTopBtn = document.getElementById("scroll-top-btn");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.remove("hidden");
        } else {
            scrollTopBtn.classList.add("hidden");
        }
    });

    scrollTopBtn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // --------- DARK MODE TOGGLE LOGIC ---------
    const themeSwitch = document.getElementById("theme-switch");
    const currentTheme = localStorage.getItem("theme");

    if (currentTheme === "dark") {
        document.body.classList.add("dark-mode");
        themeSwitch.checked = true;
    }

    themeSwitch.addEventListener("change", () => {
        if (themeSwitch.checked) {
            document.body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark");
        } else {
            document.body.classList.remove("dark-mode");
            localStorage.setItem("theme", "light");
        }
    });
    // --------------------------------------------
});

const processResponse = (jsonData) => {
    console.log("Response received:", jsonData);

    midTextElement = document.getElementById("mid-text");
    postTextElement = document.getElementById("post-text");
    summaryElement = document.getElementById("summary");
    citationsElement = document.getElementById("citations");
    summaryData = jsonData["summary"]
    citationsData = jsonData["abstracts"]

    citedIds = citationsData.map(citation => citation["id"]);

    // Process the summary
    processSummary(summaryElement, summaryData, citedIds);

    // Process the citations
    processCitations(citationsElement, citationsData);

    // Once processing is done, hide the loader and show the final result.
    midTextElement.classList.remove("not-hidden");
    midTextElement.classList.add("hidden");

    console.log("Loader hidden");

    postTextElement.classList.remove("hidden");
    postTextElement.classList.add("not-hidden");

    // Expand the summary section to full viewport height and smoothly scroll it into view.
    postTextElement.style.minHeight = "100vh";
    window.scrollTo({
        top: summaryElement.offsetTop - 100, // adjust offset if needed
        behavior: "smooth"
    });
}

const processSummary = (summaryElement, summaryData, citedIds) => {
    console.log(citedIds);

    // Escape special characters in IDs for regex usage
    const safeIds = citedIds.map(id => id.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&'));

    // Create a regex to match any of the citation IDs surrounded by square brackets
    const citationRegex = new RegExp(`\\[(${safeIds.join("|")})\\]`, "g");

    // Replace matched citation IDs with anchor tags pointing to the corresponding citation block
    const processedSummary = summaryData.replace(citationRegex, (match, id) => {
        return `<u><a href="#citation-${id}" class="citation-inline">[${id}]</a></u>`;
    });

    summaryElement.innerHTML = processedSummary;
}

const processCitations = (citationsElement, citationsData) => {
    // Clear previous citations
    citationsElement.innerHTML = "";

    citationsData.forEach((citation, index) => {
        const { id, title, authors, year, abstract, pdf_url } = citation;

        const wrapper = document.createElement("div");
        wrapper.classList.add("citation-card");
        wrapper.id = `citation-${id}`

        const header = document.createElement("div");
        header.classList.add("citation-header");

        const titleElement = document.createElement("h2");
        titleElement.classList.add("citation-title");
        titleElement.textContent = `${id} — ${title}`;

        authorsJoined = shrinkAuthors(authors);

        const meta = document.createElement("p");
        meta.classList.add("citation-meta");
        meta.textContent = `${year} — ${authorsJoined}`;

        const link = document.createElement("a");
        link.classList.add("citation-link");
        link.href = pdf_url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = "PDF";

        const toggleBtn = document.createElement("button");
        toggleBtn.classList.add("abstract-toggle");
        toggleBtn.textContent = "Show Abstract";

        const abstractBox = document.createElement("div");
        abstractBox.classList.add("abstract-box", "hidden");
        abstractBox.textContent = abstract;

        toggleBtn.addEventListener("click", () => {
            abstractBox.classList.toggle("hidden");
            toggleBtn.textContent = abstractBox.classList.contains("hidden") ? "Show Abstract" : "Hide Abstract";
        });

        header.appendChild(titleElement);
        header.appendChild(meta);
        header.appendChild(link);
        header.appendChild(toggleBtn);

        wrapper.appendChild(header);
        wrapper.appendChild(abstractBox);
        citationsElement.appendChild(wrapper);
    });
}

const shrinkAuthors = (authors) => {
    if (authors.length <= 3) {
        return authors.join(", ");
    } else {
        return `${authors.slice(0, 3).join(", ")}, et al.`;
    }
}