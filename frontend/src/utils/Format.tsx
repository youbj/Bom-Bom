export const formatPhoneNumber = (input: string): string => {
  const numbers = input.replace(/[^\d]/g, '').slice(0, 11);

  if (numbers.length < 4) return numbers;
  if (numbers.length < 8) return `${numbers.slice(0, 3)} - ${numbers.slice(3)}`;
  return `${numbers.slice(0, 3)}-${numbers.slice(3, 7)}-${numbers.slice(7)}`;
};

export const formatBirth = (input: string) => {
  const births = input.replace(/[^\d]/g, '');
  const limitedBirths = births.slice(0, 8);

  if (limitedBirths.length < 5) return births;
  if (limitedBirths.length < 7)
    return `${limitedBirths.slice(0, 4)}-${limitedBirths.slice(4)}`;
  return `${limitedBirths.slice(0, 4)}-${limitedBirths.slice(
    4,
    6,
  )}-${limitedBirths.slice(6)}`;
};

export const formatTime = (input: string) => {
  const time = input.replace(/[^\d]/g, '');
  const limitedTime = time.slice(0, 4);

  if (limitedTime.length < 3) return time;

  return `${limitedTime.slice(0, 2)}:${limitedTime.slice(2)}`;
};
