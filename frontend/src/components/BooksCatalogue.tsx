import { useState, useEffect } from 'react';
import { IBook } from '../types';
import { getBooks, getBook } from '../api/BooksApi';
import { getRecommendedBooksToQuery, getRecommendedBooksToUser } from '../api/RecommendationApi';
import BooksGrid from './BooksGrid';
import { Box, CircularProgress } from '@mui/material';
import BooksSearchBar from './BooksSearchBar';

const BooksCatalogue = ({ userId }: { userId: string }) => {

    const [books, setBooks] = useState<IBook[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);
    const [searchByQuery, setSearchByQuery] = useState(false);

    const pageSize = 12;

    const fetchBooks = async () => {
        getBooks(pageSize, (page - 1) * pageSize, search)
            .then(data => setBooks(data))
            .catch(err => {
                console.log(err);
                setBooks([]);
            })
            .finally(() => setLoading(false))
    };

    const fetchBooksByQuery = async () => {
        getRecommendedBooksToQuery(search, pageSize, (page - 1))
            .then(async data => {
                const promises = await data.map(async rec => getBook(rec.bookId));
                const values = await Promise.all(promises);
                setBooks(values)
            })
            .catch(err => {
                console.log(err);
                setBooks([]);
            })
            .finally(() => setLoading(false))
    }

    const fetchBooksByUser = async () => {
        getRecommendedBooksToUser(userId, pageSize, (page - 1))
            .then(async data => {
                const promises = await data.map(async rec => getBook(rec.bookId));
                const values = await Promise.all(promises);

                if (values.length > 0) { setBooks(values); }
                else { fetchBooks() } //recommend most popular

            })
            .catch(err => {
                console.log(err);
                setBooks([]);
            })
            .finally(() => setLoading(false))
    }

    useEffect(() => {
        if (search) {
            searchByQuery ? fetchBooksByQuery() : fetchBooks();
        }
        else if (userId) {
            fetchBooksByUser();
        } else {
            fetchBooks();
        }

    }, [userId, search, page]);

    const content = (loading) ? <CircularProgress /> : <BooksGrid books={books} />;

    return (
        <>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 2, p: 2 }}>
                <BooksSearchBar actualPage={page} setPage={setPage} searchByQuery={searchByQuery} setSearchByQuery={setSearchByQuery} setSearch={setSearch} nextPageDisabled={books.length < pageSize} />
                {content}
            </Box>
        </>
    );
}

export default BooksCatalogue;