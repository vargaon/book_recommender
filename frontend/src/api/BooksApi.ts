import { IBook } from "../types";

interface IBackendBook {
    book_id: string;
    title: string;
    description: string;
    image_url: string;
    authors: string[];
    genres: string[];
}

const mapToBook = (book: IBackendBook): IBook => {
    return { id: book.book_id, title: book.title, description: book.description, imageUrl: book.image_url, authors: book.authors, genres: book.genres }
}

export const getBooks = async (limit: number = 10, offset: number = 0, title: string | null = null) => {
    const params = new URLSearchParams({
        'limit': limit.toString(),
        'offset': offset.toString(),
    });

    title && params.append('title', `\"${title}\"`);

    const response = await fetch(`http://localhost:8080/api/books?${params}`, {
        method: 'GET',
    });

    const data = await response.json();

    return data.books.map(mapToBook) as IBook[];
}

export const getBook = async (id: string) => {
    const response = await fetch(`http://localhost:8080/api/books/${id}`, {
        method: 'GET',
    });

    const data = await response.json();

    return mapToBook(data);
}