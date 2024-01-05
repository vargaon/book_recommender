import { IBookRecommendation } from "../types";

interface IBackendBookRecommendation {
    book_id: string;
    score: number;
}

const mapToBookRecommendation = (recommendation: IBackendBookRecommendation): IBookRecommendation => {
    return { bookId: recommendation.book_id, score: recommendation.score }
}

export const getRecommendedBooksToUser = async (userId: string, count: number = 10, iter: number = 0) => {
    const params = new URLSearchParams({
        'count': count.toString(),
        'iter': iter.toString(),
    });

    const response = await fetch(`http://localhost:8080/api/recommendation/books2user/${userId}?${params}`, {
        method: 'GET',
    });

    const data = await response.json();

    return data.recommendation.map(mapToBookRecommendation) as IBookRecommendation[];
}

export const getRecommendedBooksToBook = async (bookId: string, count: number = 10, iter: number = 0) => {
    const params = new URLSearchParams({
        'count': count.toString(),
        'iter': iter.toString(),
    });

    const response = await fetch(`http://localhost:8080/api/recommendation/books2book/${bookId}?${params}`, {
        method: 'GET',
    });

    const data = await response.json();

    return data.recommendation.map(mapToBookRecommendation) as IBookRecommendation[];
}

export const getRecommendedBooksToQuery = async (query: string, count: number = 10, iter: number = 0) => {
    const params = new URLSearchParams({
        'query': query,
        'count': count.toString(),
        'iter': iter.toString(),
    });

    const response = await fetch(`http://localhost:8080/api/recommendation/books2query?${params}`, {
        method: 'GET',
    });

    const data = await response.json();

    return data.recommendation.map(mapToBookRecommendation) as IBookRecommendation[];
}