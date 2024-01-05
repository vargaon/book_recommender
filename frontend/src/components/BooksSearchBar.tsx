import { Paper, IconButton, InputBase, Switch } from "@mui/material"
import SearchIcon from '@mui/icons-material/Search';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ClearIcon from '@mui/icons-material/Clear';

import { useState } from "react";

const BooksSearchBar = ({ actualPage, setPage, searchByQuery, setSearchByQuery, setSearch, nextPageDisabled }:
    {
        actualPage: number;
        setPage: (page: number) => void;
        searchByQuery: boolean;
        setSearchByQuery: (searchByQuery: boolean) => void;
        setSearch: (search: string) => void;
        nextPageDisabled: boolean
    }) => {

    const [searchValue, setSearchValue] = useState("");

    const handleNextPage = () => {
        setPage(actualPage + 1);
    };

    const handlePrevPage = () => {
        if (actualPage > 1) setPage(actualPage - 1);
    };

    const handleSearchClick = () => {
        setPage(1);
        setSearch(searchValue);
    };

    const handleClearSearch = () => {
        setSearchValue("");
    };

    return (
        <Paper component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}>
            <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={handleSearchClick}>
                <SearchIcon />
            </IconButton>
            <InputBase placeholder={searchByQuery ? "Description" : "Title"} value={searchValue} sx={{ ml: 1, flex: 1 }} name="search" onChange={(e) => { setSearchValue(e.target.value) }} />
            <IconButton type="button" sx={{ p: '10px' }} aria-label="clear" onClick={handleClearSearch} disabled={searchValue ? false : true}>
                <ClearIcon />
            </IconButton>
            <Switch onChange={(e) => { setSearchByQuery(e.target.checked) }} />
            <IconButton type="button" sx={{ p: '10px' }} aria-label="prev-page" onClick={handlePrevPage} disabled={actualPage < 2}>
                <ArrowBackIosIcon />
            </IconButton>
            <IconButton type="button" sx={{ p: '10px' }} aria-label="next-page" onClick={handleNextPage} disabled={nextPageDisabled}>
                <ArrowForwardIosIcon />
            </IconButton>
        </Paper>
    )
}

export default BooksSearchBar;