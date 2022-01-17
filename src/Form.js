import React, { useState } from "react";

// credit to https://github.com/mdn/todo-react/blob/master/src/
// mozilla react to-do app starter code

function Form(props) {
    const [name, setName] = useState('');


    function handleSubmit(e) {
        e.preventDefault();
        if (!name.trim()) {
            return;
        }
        props.addStatement(name);
        setName("");
    }


    function handleChange(e) {
        setName(e.target.value);
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                id="new-statement-input"
                className="input input__lg"
                name="text"
                autoComplete="off"
                value={name}
                onChange={handleChange}
                placeholder="What's up?"
            />
            <button type="submit" className="btn btn__primary btn__lg">
                Submit
            </button>
        </form>
    );
}

export default Form;