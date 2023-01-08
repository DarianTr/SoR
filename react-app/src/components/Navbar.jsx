import styled from '@emotion/styled';
import { AppBar, Toolbar, Typography } from '@mui/material';
import React from "react";

const StyledToolbar = styled(Toolbar)({
  display:"flex",
  justifyContent:'space-between'
})

const Navbar = (props) => {
  return(
    <AppBar postion="sticky" color="primary">
      <StyledToolbar>
        <Typography>{props.name}</Typography>
      </StyledToolbar>
    </AppBar>
  );
};

export default Navbar;