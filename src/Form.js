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
        <form onSubmit={handleSubmit} class = "textbox">
            <input
                type="text"
                id="new-statement-input"
                className="input-large"
                name="text"
                autoComplete="off"
                value={name}
                onChange={handleChange}
                placeholder = "I feel..."
                class = "text"
            />
            <form type="submit" className="btn btn__primary btn__lg">

            </form>
        </form>
    );
}

export default Form;