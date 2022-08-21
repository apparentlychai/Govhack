import React, { useEffect, useState } from "react";
import { MenuItem2 } from "@blueprintjs/popover2";
import { ItemRenderer, ItemPredicate, Suggest2 } from "@blueprintjs/select";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";


export interface Address {
  address: string;
  lat: number;
  lon: number;
}

/** Example addresses for testing */
const addresses: Address[] = [
  { address: "Testing", lat: 19.123, lon: 20.178 },
  { address: "Apple St", lat: 31.123, lon: -18.178 },
];

const addToString = (add: Address) => add.address;

const renderAddress: ItemRenderer<Address> = (add, { handleClick, handleFocus, modifiers }) => {
  if (!modifiers.matchesPredicate) {
      return null;
  }
  return (
      <MenuItem2
          text={add.address}
          label={add.address}
          roleStructure="listoption"
          active={modifiers.active}
          key={add.address}
          onClick={handleClick}
          onFocus={handleFocus}
      />
  );
};


const AddressSuggest = Suggest2.ofType<Address>();

const Autocomplete = () => {

    const [value, setValue] = useState(addresses[0]);
    useEffect(() => Streamlit.setFrameHeight());
    const opts = {
      closeOnSelect: true,
      fill: false,
      address: value,
    }

    return (
      <AddressSuggest
        {...opts}
        inputValueRenderer={addToString}
        items={addresses} // TODO: extend state to include address list
        //itemPredicate={filterAddress}
        itemRenderer={renderAddress}
        noResults={<MenuItem2 disabled={true} text="No addresses found." roleStructure="listoption" />}
        onItemSelect={(add: Address) => add && setValue(add)}
        //popoverProps={{ matchTargetWidth: true, minimal: true }}
    />
    );
}

export default withStreamlitConnection(Autocomplete);
