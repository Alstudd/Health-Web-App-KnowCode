function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/note";
    });
}

// function deleteTodo(noteId) {
//     fetch('/delete-note', {
//         method: 'POST',
//         body: JSON.stringify({ noteId: noteId })
//     }).then((_res) => {
//         window.location.href = "/todo";
//     });
// }