import os
import streamlit.components.v1 as components

# flag to manage local dev
_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "autocomplete_component",
        url="http://localhost:3001",  # local address of node server when hotloading
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("autocomplete_component", path=build_dir)


def autocomplete_component(address, key=None):
    component_value = _component_func(address=address, key=key, default=0)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run autocomplete_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.subheader("Component test")
    add_input = st.text_input("Enter an address", value="Streamlit")
    suggestions = autocomplete_component(add_input, key="address")
    st.markdown(suggestions)