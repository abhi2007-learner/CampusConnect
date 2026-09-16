async function loadEvents() {

    const response = await fetch("http://127.0.0.1:5000/api/events");

    const events = await response.json();

    const eventGrid = document.getElementById("eventGrid");

    if (!eventGrid) {

        return;

    }

    eventGrid.innerHTML = "";

    events.forEach(event => {
    let image = "images/tech-fest.png";

if (event.title.trim().toLowerCase() === "coding competition") { 
    image = "images/coding.png";
}

if (event.title.trim().toLowerCase() === "cultural night") {
    image = "images/cultural-night.png";
}

if (event.title.trim().toLowerCase() === "annual sports meet") {
    image = "images/sports-meet.png";
}


        const card = document.createElement("div");

        card.className = "event-card";

        card.innerHTML = `
    <div class="event-image">
       <img src="${image}">
    </div>

    <div class="event-info">
        <span class="event-category">Campus Event</span>

        <h2>${event.title}</h2>

        <p>📅 ${event.date}</p>

        <p>${event.description}</p>

        <button class="register-btn"
            onclick="registerForEvent(${event.id})">
            Register
        </button>
    </div>
`;

        eventGrid.appendChild(card);

    });

}

loadEvents();

async function registerForEvent(eventId) {

   const studentName = localStorage.getItem("userName");

const studentEmail = localStorage.getItem("userEmail");

    if (!studentName || !studentEmail) {

        alert("Please enter both name and email.");

        return;

    }

    const response = await fetch("http://127.0.0.1:5000/api/register", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            event_id: eventId,

            student_name: studentName,

            student_email: studentEmail

        })

    });

    const data = await response.json();

    alert(data.message);

}

async function loadCommunityPosts() {

    const response = await fetch("http://127.0.0.1:5000/api/community");

    const posts = await response.json();

    const postsContainer = document.getElementById("posts");

    if (!postsContainer) {

        return;

    }

    postsContainer.innerHTML = "";

    posts.forEach(async post => {

        const postCard = document.createElement("article");

        postCard.className = "post-card";

        postCard.innerHTML = `

            <div class="post-header">

                <div class="avatar">${post.author.charAt(0)}</div>

                <div>

                    <h3>${post.author}</h3>

                    <span>${post.date}</span>

                </div>

            </div>

            <p class="post-text">

                ${post.content}

            </p>

            <div class="post-actions">

                <button>❤️ Like</button>

                <button onclick="addComment(${post.id})">💬 Comment</button>

            </div>

        `;

        postsContainer.appendChild(postCard);

        const commentResponse = await fetch(

     `http://127.0.0.1:5000/api/comments/${post.id}`

);

const comments = await commentResponse.json();

comments.forEach(comment => {

    const commentElement = document.createElement("p");

    commentElement.innerHTML = `

        💬 <strong>${comment.author}:</strong> ${comment.content}

    `;

    postCard.appendChild(commentElement);

});

    });

}

loadCommunityPosts();

document.querySelector(".post-btn")?.addEventListener("click", async function () {

    const authorInput = document.getElementById("author");

    const contentInput = document.getElementById("content");

    const author = authorInput.value.trim();

    const content = contentInput.value.trim();

    if (!author || !content) {

        alert("Please enter your name and write something.");

        return;

    }

    const response = await fetch("http://127.0.0.1:5000/api/community", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            author: author,

            content: content,

            date: new Date().toISOString().split("T")[0]

        })

    });

    const data = await response.json();

    alert(data.message);

    authorInput.value = "";

    contentInput.value = "";

    loadCommunityPosts();

});

async function addComment(postId) {

    const author = prompt("Enter your name:");

    const content = prompt("Write your comment:");

    if (!author || !content) {

        alert("Please enter both name and comment.");

        return;

    }

    const response = await fetch("http://127.0.0.1:5000/api/comments", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            post_id: postId,

            author: author,

            content: content,

            date: new Date().toISOString().split("T")[0]

        })

    });

    const data = await response.json();

    alert(data.message);

}

document.getElementById("signupForm")?.addEventListener("submit", async function(event) {

    event.preventDefault();

    const name = document.getElementById("name").value.trim();

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/api/signup", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            name: name,

            email: email,

            password: password

        })

    });

    const data = await response.json();

    alert(data.message);

    if (response.ok) {

        document.getElementById("signupForm").reset();

    }

});

document.getElementById("loginForm")?.addEventListener("submit", async function(event) {

    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();

    const password = document.getElementById("loginPassword").value;

    const response = await fetch("http://127.0.0.1:5000/api/login", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            email: email,

            password: password

        })

    });

    const data = await response.json();

    alert(data.message);

    if (response.ok) {

        localStorage.setItem("userName", data.name);

        localStorage.setItem("userEmail", email);  

        window.location.href="profile.html";

    }

});

const profileName = document.getElementById("profileName");

const userEmail = localStorage.getItem("userEmail");

if (userEmail) {

    fetch(`http://127.0.0.1:5000/api/profile?email=${encodeURIComponent(userEmail)}`)

        .then(response => response.json())

        .then(data => {

    const profileEmail = document.getElementById("profileEmail");

    const profileCourse = document.getElementById("profileCourse");

const profileYear = document.getElementById("profileYear");

if (profileCourse) {

    profileCourse.textContent = data.course;

}

if (profileYear) {

    profileYear.textContent = data.year;

}

if (profileBio) {

    profileBio.textContent = data.bio;

}

    if (profileEmail) {

        profileEmail.textContent = data.email;

    }

});

}

const editProfileBtn = document.getElementById("editProfileBtn");

const editProfileForm = document.getElementById("editProfileForm");

if (editProfileBtn && editProfileForm) {

   editProfileBtn.addEventListener("click", function () {

    editProfileForm.style.display = "block";

    document.getElementById("editCourse").value =

        document.getElementById("profileCourse").textContent;

    document.getElementById("editYear").value =

        document.getElementById("profileYear").textContent;

    document.getElementById("editBio").value =

        document.getElementById("profileBio").textContent;

});

}

const saveProfileBtn = document.getElementById("saveProfileBtn");

if (saveProfileBtn) {

    saveProfileBtn.addEventListener("click", async function () {

        const email = localStorage.getItem("userEmail");

        const course = document.getElementById("editCourse").value;

        const year = document.getElementById("editYear").value;

        const bio = document.getElementById("editBio").value;

        const response = await fetch("http://127.0.0.1:5000/api/profile", {

            method: "PUT",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email,

                course: course,

                year: year,

                bio: bio

            })

        });

        const data = await response.json();

        alert(data.message);

        document.getElementById("profileCourse").textContent = course;

document.getElementById("profileYear").textContent = year;

document.getElementById("profileBio").textContent = bio;

editProfileForm.style.display = "none";

    });

}

const noticeList = document.getElementById("noticeList");

if (noticeList) {

    fetch("http://127.0.0.1:5000/api/notices")

        .then(response => response.json())

        .then(data => {

            noticeList.innerHTML = "";

            data.forEach(notice => {

                const noticeBox = document.createElement("div");

                noticeBox.className = "notice-box";

                noticeBox.innerHTML = `

                    <div class="notice-icon">

                        📢

                    </div>

                    <div class="notice-content">

                        <span class="notice-date">

                            ${notice.date}

                        </span>

                        <h2>${notice.title}</h2>

                        <p>

                            ${notice.content}

                        </p>

                    </div>

                `;

                noticeList.appendChild(noticeBox);

            });

        })

        .catch(error => {

            console.error("Error loading notices:", error);

        });

}

const notificationList = document.getElementById("notificationList");

if (notificationList) {

    fetch("http://127.0.0.1:5000/api/notifications")

        .then(response => response.json())

        .then(data => {

            notificationList.innerHTML = "";

            data.forEach(notification => {

                const notificationBox = document.createElement("div");

                notificationBox.className = "notice-box";

                notificationBox.innerHTML = `

                    <div class="notice-icon">

                        📢

                    </div>

                    <div class="notice-content">

                        <span class="notice-date">

                            ${notification.date}

                        </span>

                        <h2>${notification.title}</h2>

                        <p>

                            ${notification.content}

                        </p>

                    </div>

                `;

                notificationList.appendChild(notificationBox);

            });

        })

        .catch(error => {

            console.error("Error loading notifications:", error);

        });

}

const addNoticeBtn = document.getElementById("addNoticeBtn");

if (addNoticeBtn) {

    addNoticeBtn.addEventListener("click", async function () {

        const title = document.getElementById("noticeTitle").value;

        const content = document.getElementById("noticeContent").value;

        const date = document.getElementById("noticeDate").value;

        if (!title || !content || !date) {

            alert("Please fill all fields.");

            return;

        }

        const response = await fetch(

            "http://127.0.0.1:5000/api/admin/notices",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    title: title,

                    content: content,

                    date: date

                })

            }

        );

        const data = await response.json();

        alert(data.message);

        if (response.ok) {

            document.getElementById("noticeTitle").value = "";

            document.getElementById("noticeContent").value = "";

            document.getElementById("noticeDate").value = "";

        }

    });

}
const addEventBtn = document.getElementById("addEventBtn");

if (addEventBtn) {
    addEventBtn.addEventListener("click", async function () {

        const title = document.getElementById("eventTitle").value;
        const description = document.getElementById("eventDescription").value;
        const date = document.getElementById("eventDate").value;

        if (!title || !description || !date) {
            alert("Please fill all fields.");
            return;
        }

        const response = await fetch(
            "http://127.0.0.1:5000/api/admin/events",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    date: date
                })
            }
        );

        const data = await response.json();

        alert(data.message);

        if (response.ok) {
            document.getElementById("eventTitle").value = "";
            document.getElementById("eventDescription").value = "";
            document.getElementById("eventDate").value = "";
        }
    });
}