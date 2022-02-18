const createFormButton = document.getElementById('create-form')

function createQuestionForm(id) {
    return `
        <div class="rounded shadow">
        <div class="m-3">
            <div class="form-floating mb-3">
                <input class="form-control"
                       id="quiz-title-form"
                       aria-describedby="Question"
                       name="NEW_QUESTION${id}"
                       placeholder="Question">
                <label for="quiz-title-form">Question</label>
            </div>
            <ul>
                <li>
                    <div class="form-floating mb-3">
                        <input class="form-control"
                               id="quiz-title-form"
                               aria-describedby="Option"
                               name="NEW_OPTION${id}"
                               placeholder="Option">
                        <label for="quiz-title-form" class="form-label">Option</label>
                    </div>
                </li>
            </ul>
        </div>
        </div>
    `
}

document.getElementById('submit-button')
    .addEventListener('click', () => {
        createFormButton.submit()
    })

document.getElementById('add-question')
    .addEventListener('click', () => {
        let questionCreateForm = document.createElement('div')
        questionCreateForm.innerHTML = createQuestionForm(Math.floor(Math.random() * 10000))

        createFormButton.insertBefore(
            questionCreateForm,
            document.getElementById('add-question'))
    })

const buttons = document.querySelectorAll('button')

for (let button of buttons) {
    // check if the button is a delete button
    if (button.getAttribute('data-id') !== null) {
        button.addEventListener('click', () => {
            document.getElementById(button.getAttribute('data-id')).remove()
        })
    }

    // check if the button is an add option button
    if (button.getAttribute('data-question-id') !== null) {
        button.addEventListener('click', () => {
            const optionForm = document.createElement('li')
            optionForm.innerHTML = `
                <div class="input-group">
                    <div class="form-floating mb-3">
                        <input class="form-control"
                               id="quiz-option"
                               aria-describedby="Option"
                               name="NEW_OPTION"
                               value="">
                        <label for="quiz-option"
                               class="form-label">Option</label>
                    </div>
                </div>`

            document.getElementById(
                `OPTIONS${button.getAttribute('data-question-id')}`
            ).insertBefore(
                optionForm,
                document.getElementById('add-option-li')
            )
        })
    }
}