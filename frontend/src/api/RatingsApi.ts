import { IUserRating } from "../types";

interface IBackendUserRating {
    book_id: string;
    rating: number;
}

const mapToUserRating = (rating: IBackendUserRating): IUserRating => {
    return { bookId: rating.book_id, rating: rating.rating }
}

export const getUserRatings = async (userId: string, limit: number = 10, offset: number = 0) => {
    const params = new URLSearchParams({
        'limit': limit.toString(),
        'offset': offset.toString(),
    });

    const response = await fetch(`http://localhost:8080/api/ratings/user/${userId}?${params}`, {
        method: 'GET',
    });

    const data = await response.json();

    return data.ratings.map(mapToUserRating) as IUserRating[];
}

export const getUserRatingOfBook = async (userId: string, bookId: string): Promise<IUserRating | null> => {
    const response = await fetch(`http://localhost:8080/api/ratings/user/${userId}/book/${bookId}`, {
        method: 'GET',
    });

    if (response.ok) {
        const data = await response.json();
        return mapToUserRating(data);
    }

    return null;
}

export const createUserRating = async (userId: string, bookId: string, rating: number): Promise<void> => {
    const body = { book_id: bookId, rating: rating };

    const response = await fetch(`http://localhost:8080/api/ratings/user/${userId}`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    return await response.json()
}

export const removeUserRating = async (userId: string, bookId: string): Promise<void> => {
    await fetch(`http://localhost:8080/api/ratings/user/${userId}/book/${bookId}`, {
        method: 'DELETE',
    });
}